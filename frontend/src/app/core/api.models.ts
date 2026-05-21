export type UserRole = 'admin' | 'student';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  is_active: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: 'bearer';
  user: User;
}

export interface CourseSummary {
  id: string;
  title: string;
  phase: number;
  lesson_count: number;
  completed_count: number;
  progress_percent: number;
}

export interface RoadmapPhase {
  id: number;
  title: string;
  courses: CourseSummary[];
}

export interface RoadmapResponse {
  phases: RoadmapPhase[];
}

export interface CourseLessonSummary {
  id: string;
  title: string;
  description: string | null;
  order: number;
  level: string;
  estimated_minutes: number;
  tags: string[];
  status: string;
  progress_percent: number;
}

export interface CourseDetail {
  id: string;
  title: string;
  phase: number;
  lesson_count: number;
  completed_count: number;
  progress_percent: number;
  lessons: CourseLessonSummary[];
}

export interface LessonProgress {
  lesson_id: string;
  status: string;
  progress_percent: number;
  last_position: string | null;
  last_viewed_at: string | null;
  completed_at: string | null;
}

export interface PublicQuiz {
  id: string;
  type: 'fill_blank' | 'code_output' | 'short_answer';
  question: string;
}

export interface Lesson {
  id: string;
  course_id: string;
  title: string;
  description: string | null;
  phase: number;
  order: number;
  level: string;
  estimated_minutes: number;
  tags: string[];
  body: string;
  quizzes: PublicQuiz[];
  progress: LessonProgress | null;
}
