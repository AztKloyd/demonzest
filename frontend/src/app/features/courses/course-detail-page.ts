import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { CourseDetail } from '../../core/api.models';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-course-detail-page',
  imports: [RouterLink],
  templateUrl: './course-detail-page.html',
  styleUrl: './course-detail-page.scss',
})
export class CourseDetailPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly auth = inject(AuthService);
  private readonly route = inject(ActivatedRoute);

  readonly course = signal<CourseDetail | null>(null);
  readonly error = signal('');
  readonly loading = signal(true);

  ngOnInit() {
    const token = this.auth.token;
    const courseId = this.route.snapshot.paramMap.get('courseId');

    if (!token || !courseId) {
      this.loading.set(false);
      this.error.set('Course could not be opened.');
      return;
    }

    this.api.course(token, courseId).subscribe({
      next: (course) => {
        this.course.set(course);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Course could not be loaded.');
        this.loading.set(false);
      },
    });
  }
}
