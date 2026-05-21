import { inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { tap } from 'rxjs';

import { ApiService } from './api.service';
import { User } from './api.models';

const TOKEN_KEY = 'demonzest.accessToken';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);

  readonly currentUser = signal<User | null>(null);

  get token() {
    return localStorage.getItem(TOKEN_KEY);
  }

  get isLoggedIn() {
    return this.token !== null;
  }

  login(email: string, password: string) {
    return this.api.login(email, password).pipe(
      tap((response) => {
        localStorage.setItem(TOKEN_KEY, response.access_token);
        this.currentUser.set(response.user);
      }),
    );
  }

  loadMe() {
    const token = this.token;
    if (!token) {
      return null;
    }

    return this.api.me(token).pipe(
      tap((user) => {
        this.currentUser.set(user);
      }),
    );
  }

  logout() {
    localStorage.removeItem(TOKEN_KEY);
    this.currentUser.set(null);
    this.router.navigateByUrl('/login');
  }
}
