import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';
import { Lesson } from '../../core/api.models';

@Component({
  selector: 'app-lesson-page',
  imports: [RouterLink],
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
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Lesson could not be loaded.');
        this.loading.set(false);
      },
    });
  }
}
