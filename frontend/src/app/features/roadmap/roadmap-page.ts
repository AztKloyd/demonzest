import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { RoadmapResponse } from '../../core/api.models';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-roadmap-page',
  imports: [RouterLink],
  templateUrl: './roadmap-page.html',
  styleUrl: './roadmap-page.scss',
})
export class RoadmapPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly auth = inject(AuthService);

  readonly roadmap = signal<RoadmapResponse | null>(null);
  readonly error = signal('');
  readonly loading = signal(true);

  ngOnInit() {
    const token = this.auth.token;
    if (!token) {
      this.loading.set(false);
      this.error.set('Login is required.');
      return;
    }

    this.api.roadmap(token).subscribe({
      next: (roadmap) => {
        this.roadmap.set(roadmap);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Roadmap could not be loaded.');
        this.loading.set(false);
      },
    });
  }
}
