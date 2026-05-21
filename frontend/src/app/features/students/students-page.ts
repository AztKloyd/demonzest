import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { ApiService } from '../../core/api.service';
import { UserProgress, UserRole } from '../../core/api.models';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-students-page',
  imports: [FormsModule],
  templateUrl: './students-page.html',
  styleUrl: './students-page.scss',
})
export class StudentsPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly auth = inject(AuthService);

  readonly users = signal<UserProgress[]>([]);
  readonly loading = signal(true);
  readonly saving = signal(false);
  readonly error = signal('');
  readonly message = signal('');

  readonly form = signal({
    email: '',
    password: '',
    name: '',
    role: 'student' as UserRole,
  });

  ngOnInit() {
    this.loadUsers();
  }

  updateField(field: 'email' | 'password' | 'name' | 'role', value: string) {
    this.form.update((form) => ({
      ...form,
      [field]: value,
    }));
  }

  createUser() {
    const token = this.auth.token;
    const form = this.form();

    if (!token || !form.email || !form.password || !form.name) {
      this.error.set('Email, password, and name are required.');
      return;
    }

    this.saving.set(true);
    this.error.set('');
    this.message.set('');

    this.api.createUser(token, form).subscribe({
      next: (user) => {
        this.users.update((users) => [
          {
            ...user,
            lesson_count: users[0]?.lesson_count ?? 0,
            completed_count: 0,
            progress_percent: 0,
          },
          ...users,
        ]);
        this.form.set({
          email: '',
          password: '',
          name: '',
          role: 'student',
        });
        this.saving.set(false);
        this.message.set('User created.');
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.error.set(this.userCreateErrorMessage(error));
      },
    });
  }

  private loadUsers() {
    const token = this.auth.token;
    if (!token) {
      this.loading.set(false);
      this.error.set('Login is required.');
      return;
    }

    this.api.users(token).subscribe({
      next: (users) => {
        this.users.set(users);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Users could not be loaded.');
        this.loading.set(false);
      },
    });
  }

  private userCreateErrorMessage(error: unknown): string {
    if (!(error instanceof HttpErrorResponse)) {
      return 'User could not be created.';
    }

    if (error.status === 409) {
      return 'This email is already registered.';
    }

    if (error.status === 403) {
      return 'Admin permission is required.';
    }

    if (error.status === 422) {
      return 'Check the email format and use a password with at least 8 characters.';
    }

    return 'User could not be created.';
  }
}
