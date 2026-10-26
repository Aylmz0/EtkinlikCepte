/** Client-side auth session; tokens are cached for app restarts (H2.9). */
import { apiRequest } from '$lib/api/client';

export type SessionUser = {
  id: string;
  email: string;
  display_name: string;
  bio: string | null;
  city: string | null;
  interests: string[] | null;
  locale: string;
  budget_minor: number | null;
  budget_currency: string;
};

type AuthResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: SessionUser;
};

const STORAGE_KEY = 'etkinlikcepte.session';

class Session {
  accessToken = $state<string | null>(null);
  refreshToken = $state<string | null>(null);
  user = $state<SessionUser | null>(null);

  constructor() {
    if (typeof window === 'undefined') return;
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    try {
      const saved = JSON.parse(raw) as {
        access_token: string;
        refresh_token: string;
        user: SessionUser;
      };
      this.accessToken = saved.access_token;
      this.refreshToken = saved.refresh_token;
      this.user = saved.user;
    } catch {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }

  private persist(): void {
    if (typeof window === 'undefined') return;
    if (!this.accessToken || !this.refreshToken || !this.user) {
      window.localStorage.removeItem(STORAGE_KEY);
      return;
    }
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        access_token: this.accessToken,
        refresh_token: this.refreshToken,
        user: this.user
      })
    );
  }

  private accept(response: AuthResponse): void {
    this.accessToken = response.access_token;
    this.refreshToken = response.refresh_token;
    this.user = response.user;
    this.persist();
  }

  async login(email: string, password: string): Promise<void> {
    this.accept(
      await apiRequest<AuthResponse>('/auth/login', {
        method: 'POST',
        body: { email, password }
      })
    );
  }

  async register(email: string, password: string, displayName: string): Promise<void> {
    this.accept(
      await apiRequest<AuthResponse>('/auth/register', {
        method: 'POST',
        body: { email, password, display_name: displayName }
      })
    );
  }

  async refresh(): Promise<void> {
    if (!this.refreshToken) return;
    const response = await apiRequest<{
      access_token: string;
      refresh_token: string;
    }>('/auth/refresh', { method: 'POST', body: { refresh_token: this.refreshToken } });
    this.accessToken = response.access_token;
    this.refreshToken = response.refresh_token;
    this.persist();
  }

  logout(): void {
    this.accessToken = null;
    this.refreshToken = null;
    this.user = null;
    this.persist();
  }
}

export const session = new Session();
