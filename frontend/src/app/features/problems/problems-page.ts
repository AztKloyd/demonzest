import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { ProblemSummary } from '../../core/api.models';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-problems-page',
  imports: [RouterLink],
  templateUrl: './problems-page.html',
  styleUrl: './problems-page.scss',
})
export class ProblemsPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly auth = inject(AuthService);

  readonly problems = signal<ProblemSummary[]>([]);
  readonly loading = signal(true);
  readonly error = signal('');

  ngOnInit() {
    const token = this.auth.token;
    if (!token) {
      this.loading.set(false);
      this.error.set('Login is required.');
      return;
    }

    this.api.problems(token).subscribe({
      next: (response) => {
        this.problems.set(response.problems);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Problems could not be loaded.');
        this.loading.set(false);
      },
    });
  }
}
