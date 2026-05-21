import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';
import { RoadmapResponse, User } from '../../core/api.models';

@Component({
  selector: 'app-dashboard-page',
  imports: [RouterLink],
  templateUrl: './dashboard-page.html',
  styleUrl: './dashboard-page.scss',
})
export class DashboardPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly auth = inject(AuthService);

  protected readonly user = signal<User | null>(this.auth.currentUser());
  protected readonly roadmap = signal<RoadmapResponse | null>(null);
  protected readonly error = signal('');

  ngOnInit() {
    const request = this.auth.loadMe();
    request?.subscribe((user) => this.user.set(user));

    const token = this.auth.token;
    if (!token) {
      return;
    }

    this.api.roadmap(token).subscribe({
      next: (roadmap) => this.roadmap.set(roadmap),
      error: () => this.error.set('Progress summary could not be loaded.'),
    });
  }

  protected totalLessons(): number {
    return (
      this.roadmap()?.phases
        .flatMap((phase) => phase.courses)
        .reduce((total, course) => total + course.lesson_count, 0) ?? 0
    );
  }

  protected completedLessons(): number {
    return (
      this.roadmap()?.phases
        .flatMap((phase) => phase.courses)
        .reduce((total, course) => total + course.completed_count, 0) ?? 0
    );
  }

  protected courseCount(): number {
    return this.roadmap()?.phases.flatMap((phase) => phase.courses).length ?? 0;
  }

  protected overallProgress(): number {
    const total = this.totalLessons();
    if (total === 0) {
      return 0;
    }

    return Math.round((this.completedLessons() / total) * 100);
  }
}
