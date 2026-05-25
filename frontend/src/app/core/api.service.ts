import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../environments/environment';
import {
  CourseDetail,
  Lesson,
  LessonProgress,
  LessonProgressUpdateRequest,
  LoginResponse,
  ProblemDetail,
  ProblemListResponse,
  ProblemSubmission,
  ProblemSubmissionCreateRequest,
  ProblemSubmissionListResponse,
  QuizSubmitRequest,
  QuizSubmitResponse,
  RoadmapResponse,
  User,
  UserCreateRequest,
  UserProgress,
} from './api.models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = environment.apiBaseUrl;

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

  users(token: string) {
    return this.http.get<UserProgress[]>(`${this.apiBaseUrl}/users`, {
      headers: this.authHeaders(token),
    });
  }

  createUser(token: string, payload: UserCreateRequest) {
    return this.http.post<User>(`${this.apiBaseUrl}/users`, payload, {
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

  problems(token: string) {
    return this.http.get<ProblemListResponse>(`${this.apiBaseUrl}/problems`, {
      headers: this.authHeaders(token),
    });
  }

  problem(token: string, problemId: string) {
    return this.http.get<ProblemDetail>(`${this.apiBaseUrl}/problems/${problemId}`, {
      headers: this.authHeaders(token),
    });
  }

  problemSubmissions(token: string, problemId: string) {
    return this.http.get<ProblemSubmissionListResponse>(
      `${this.apiBaseUrl}/problems/${problemId}/submissions`,
      {
        headers: this.authHeaders(token),
      },
    );
  }

  submitProblem(token: string, problemId: string, payload: ProblemSubmissionCreateRequest) {
    return this.http.post<ProblemSubmission>(
      `${this.apiBaseUrl}/problems/${problemId}/submissions`,
      payload,
      {
        headers: this.authHeaders(token),
      },
    );
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

  updateProgress(token: string, lessonId: string, payload: LessonProgressUpdateRequest) {
    return this.http.put<LessonProgress>(
      `${this.apiBaseUrl}/progress/${lessonId}`,
      payload,
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
