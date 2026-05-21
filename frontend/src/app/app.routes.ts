import { Routes } from '@angular/router';

import { authGuard } from './core/auth.guard';
import { AppShell } from './layout/app-shell/app-shell';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () =>
      import('./features/login/login-page').then((m) => m.LoginPage),
  },
  {
    path: '',
    component: AppShell,
    canActivate: [authGuard],
    children: [
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/dashboard/dashboard-page').then((m) => m.DashboardPage),
      },
      {
        path: 'roadmap',
        loadComponent: () =>
          import('./features/roadmap/roadmap-page').then((m) => m.RoadmapPage),
      },
      {
        path: 'courses/:courseId',
        loadComponent: () =>
          import('./features/courses/course-detail-page').then((m) => m.CourseDetailPage),
      },
      {
        path: 'lessons/:lessonId',
        loadComponent: () =>
          import('./features/lessons/lesson-page').then((m) => m.LessonPage),
      },
      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'dashboard',
      },
    ],
  },
  {
    path: '**',
    redirectTo: 'dashboard',
  },
];
