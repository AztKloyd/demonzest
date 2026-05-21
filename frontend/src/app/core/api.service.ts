import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import {
  CourseDetail,
  Lesson,
  LessonProgress,
  LoginResponse,
  QuizSubmitRequest,
  QuizSubmitResponse,
  RoadmapResponse,
  User,
} from './api.models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000/api';

  login(email: string, password: string) {
    return this.http.post<LoginResponse>(`${this.apiBaseUrl}/auth/login`, {
      email,
      password,
    });
  }

  me(token: string) {
    return this.http.get<User>(`${this.apiBaseUrl}/me`, {
      headers: this.authHeaders(token),
    });
  }

  roadmap(token: string) {
    return this.http.get<RoadmapResponse>(`${this.apiBaseUrl}/roadmap`, {
      headers: this.authHeaders(token),
    });
  }

  course(token: string, courseId: string) {
    return this.http.get<CourseDetail>(`${this.apiBaseUrl}/courses/${courseId}`, {
      headers: this.authHeaders(token),
    });
  }

  lesson(token: string, lessonId: string) {
    return this.http.get<Lesson>(`${this.apiBaseUrl}/lessons/${lessonId}`, {
      headers: this.authHeaders(token),
    });
  }

  completeLesson(token: string, lessonId: string) {
    return this.http.post<LessonProgress>(
      `${this.apiBaseUrl}/progress/${lessonId}/complete`,
      {},
      {
        headers: this.authHeaders(token),
      },
    );
  }

  submitQuiz(token: string, lessonId: string, payload: QuizSubmitRequest) {
    return this.http.post<QuizSubmitResponse>(
      `${this.apiBaseUrl}/quiz/${lessonId}/submit`,
      payload,
      {
        headers: this.authHeaders(token),
      },
    );
  }

  private authHeaders(token: string) {
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }
}
