import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { ProblemDetail } from '../../core/api.models';
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
  readonly selectedLanguage = signal('JavaScript');
  readonly code = signal('');

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

  private defaultCode(title: string) {
    return `// ${title}\n// Judge execution will be added in a later step.\n`;
  }
}
