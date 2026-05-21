import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';
import { Lesson, QuizResult, QuizSubmitResponse } from '../../core/api.models';

type LessonBlock =
  | { type: 'heading'; level: number; text: string }
  | { type: 'paragraph'; text: string }
  | { type: 'list'; items: string[] }
  | { type: 'code'; text: string };

@Component({
  selector: 'app-lesson-page',
  imports: [FormsModule, RouterLink],
  templateUrl: './lesson-page.html',
  styleUrl: './lesson-page.scss',
})
export class LessonPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly auth = inject(AuthService);
  private readonly route = inject(ActivatedRoute);

  readonly lesson = signal<Lesson | null>(null);
  readonly error = signal('');
  readonly loading = signal(true);
  readonly completing = signal(false);
  readonly completeMessage = signal('');
  readonly quizAnswers = signal<Record<string, string>>({});
  readonly quizResult = signal<QuizSubmitResponse | null>(null);
  readonly submittingQuiz = signal(false);
  readonly quizError = signal('');
  readonly lessonBlocks = signal<LessonBlock[]>([]);

  ngOnInit() {
    const token = this.auth.token;
    const lessonId = this.route.snapshot.paramMap.get('lessonId');

    if (!token || !lessonId) {
      this.loading.set(false);
      this.error.set('Lesson could not be opened.');
      return;
    }

    this.api.lesson(token, lessonId).subscribe({
      next: (lesson) => {
        this.lesson.set(lesson);
        this.lessonBlocks.set(this.parseLessonBody(lesson.body));
        this.quizAnswers.set(
          Object.fromEntries(lesson.quizzes.map((quiz) => [quiz.id, ''])),
        );
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Lesson could not be loaded.');
        this.loading.set(false);
      },
    });
  }

  completeLesson() {
    const token = this.auth.token;
    const lesson = this.lesson();

    if (!token || !lesson) {
      return;
    }

    this.completing.set(true);
    this.completeMessage.set('');
    this.error.set('');

    this.api.completeLesson(token, lesson.id).subscribe({
      next: (progress) => {
        this.lesson.set({
          ...lesson,
          progress,
        });
        this.completing.set(false);
        this.completeMessage.set('Lesson marked as complete.');
      },
      error: () => {
        this.completing.set(false);
        this.error.set('Lesson could not be completed.');
      },
    });
  }

  setQuizAnswer(questionId: string, answer: string) {
    this.quizAnswers.update((answers) => ({
      ...answers,
      [questionId]: answer,
    }));
  }

  submitQuiz() {
    const token = this.auth.token;
    const lesson = this.lesson();

    if (!token || !lesson) {
      return;
    }

    this.submittingQuiz.set(true);
    this.quizError.set('');
    this.quizResult.set(null);

    this.api
      .submitQuiz(token, lesson.id, {
        answers: lesson.quizzes.map((quiz) => ({
          question_id: quiz.id,
          answer: this.quizAnswers()[quiz.id] ?? '',
        })),
      })
      .subscribe({
        next: (result) => {
          this.quizResult.set(result);
          this.submittingQuiz.set(false);
        },
        error: () => {
          this.quizError.set('Answers could not be submitted.');
          this.submittingQuiz.set(false);
        },
      });
  }

  resultFor(questionId: string): QuizResult | null {
    return this.quizResult()?.results.find((result) => result.question_id === questionId) ?? null;
  }

  private parseLessonBody(body: string): LessonBlock[] {
    const blocks: LessonBlock[] = [];
    const lines = body.split(/\r?\n/);
    let paragraph: string[] = [];
    let list: string[] = [];
    let code: string[] = [];
    let inCode = false;

    const flushParagraph = () => {
      if (paragraph.length > 0) {
        blocks.push({ type: 'paragraph', text: paragraph.join(' ') });
        paragraph = [];
      }
    };

    const flushList = () => {
      if (list.length > 0) {
        blocks.push({ type: 'list', items: list });
        list = [];
      }
    };

    for (const line of lines) {
      if (line.startsWith('```')) {
        if (inCode) {
          blocks.push({ type: 'code', text: code.join('\n') });
          code = [];
          inCode = false;
        } else {
          flushParagraph();
          flushList();
          inCode = true;
        }
        continue;
      }

      if (inCode) {
        code.push(line);
        continue;
      }

      const heading = /^(#{1,3})\s+(.+)$/.exec(line);
      if (heading) {
        flushParagraph();
        flushList();
        blocks.push({
          type: 'heading',
          level: heading[1].length,
          text: heading[2],
        });
        continue;
      }

      const listItem = /^-\s+(.+)$/.exec(line);
      if (listItem) {
        flushParagraph();
        list.push(listItem[1]);
        continue;
      }

      if (line.trim() === '') {
        flushParagraph();
        flushList();
        continue;
      }

      flushList();
      paragraph.push(line.trim());
    }

    flushParagraph();
    flushList();

    if (code.length > 0) {
      blocks.push({ type: 'code', text: code.join('\n') });
    }

    return blocks;
  }
}
