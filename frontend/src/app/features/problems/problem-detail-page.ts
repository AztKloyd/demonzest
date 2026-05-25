import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { ProblemDetail, ProblemSubmission } from '../../core/api.models';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-problem-detail-page',
  imports: [RouterLink],
  templateUrl: './problem-detail-page.html',
  styleUrl: './problem-detail-page.scss',
})
export class ProblemDetailPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly auth = inject(AuthService);
  private readonly route = inject(ActivatedRoute);

  readonly problem = signal<ProblemDetail | null>(null);
  readonly loading = signal(true);
  readonly error = signal('');
  readonly selectedLanguage = signal('Python');
  readonly code = signal('');
  readonly submissions = signal<ProblemSubmission[]>([]);
  readonly submitting = signal(false);
  readonly submitMessage = signal('');

  readonly bodyBlocks = computed(() => {
    const body = this.problem()?.body ?? '';
    return body.split('\n\n').filter(Boolean);
  });

  ngOnInit() {
    const token = this.auth.token;
    const problemId = this.route.snapshot.paramMap.get('problemId');
    if (!token || !problemId) {
      this.loading.set(false);
      this.error.set('Problem could not be loaded.');
      return;
    }

    this.api.problem(token, problemId).subscribe({
      next: (problem) => {
        this.problem.set(problem);
        this.code.set(this.defaultCode(problem.title));
        this.loading.set(false);
        this.loadSubmissions(token, problemId);
      },
      error: () => {
        this.error.set('Problem could not be loaded.');
        this.loading.set(false);
      },
    });
  }

  updateCode(event: Event) {
    const target = event.target as HTMLTextAreaElement;
    this.code.set(target.value);
  }

  submit() {
    const token = this.auth.token;
    const problemId = this.problem()?.id;
    if (!token || !problemId || this.submitting()) {
      return;
    }

    this.submitting.set(true);
    this.submitMessage.set('');
    this.api
      .submitProblem(token, problemId, {
        language: this.selectedLanguage(),
        code: this.code(),
      })
      .subscribe({
        next: (submission) => {
          this.submissions.set([submission, ...this.submissions()]);
          this.submitMessage.set(`Submission ${submission.status}.`);
          this.submitting.set(false);
        },
        error: () => {
          this.submitMessage.set('Submission failed.');
          this.submitting.set(false);
        },
      });
  }

  private loadSubmissions(token: string, problemId: string) {
    this.api.problemSubmissions(token, problemId).subscribe({
      next: (response) => this.submissions.set(response.submissions),
      error: () => this.submissions.set([]),
    });
  }

  private defaultCode(title: string) {
    return `# ${title}\n# Write your solution here.\n`;
  }
}
