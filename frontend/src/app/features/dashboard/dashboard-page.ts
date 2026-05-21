import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AuthService } from '../../core/auth.service';
import { User } from '../../core/api.models';

@Component({
  selector: 'app-dashboard-page',
  imports: [RouterLink],
  templateUrl: './dashboard-page.html',
  styleUrl: './dashboard-page.scss',
})
export class DashboardPage implements OnInit {
  private readonly auth = inject(AuthService);
  protected readonly user = signal<User | null>(this.auth.currentUser());

  ngOnInit() {
    const request = this.auth.loadMe();
    request?.subscribe((user) => this.user.set(user));
  }
}
