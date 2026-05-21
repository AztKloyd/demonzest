import { Component, inject, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-shell',
  imports: [RouterLink, RouterLinkActive, RouterOutlet],
  templateUrl: './app-shell.html',
  styleUrl: './app-shell.scss',
})
export class AppShell implements OnInit {
  protected readonly auth = inject(AuthService);

  ngOnInit() {
    const request = this.auth.loadMe();
    request?.subscribe();
  }

  protected isAdmin() {
    return this.auth.currentUser()?.role === 'admin';
  }
}
