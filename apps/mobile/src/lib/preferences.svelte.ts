/**
 * Reactive, localStorage-backed user preferences (theme + language).
 *
 * Frontend-only state: no backend call, no account sync. Defaults to the
 * light theme / Turkish locale when nothing is stored yet — intentionally
 * ignores the OS/browser color-scheme preference, since the app's cream
 * canvas is the default look and dark mode is an explicit opt-in from
 * Settings, not something that should flip on its own on a dark-mode device.
 * (SSR-safe: reads `localStorage` only inside `onMount`-equivalent browser checks.)
 */
import { browser } from '$app/environment';

export type Theme = 'light' | 'dark';
export type Locale = 'tr' | 'en';

const THEME_KEY = 'ec-theme';
const LOCALE_KEY = 'ec-locale';

function initialTheme(): Theme {
  if (!browser) return 'light';
  const stored = localStorage.getItem(THEME_KEY);
  return stored === 'dark' ? 'dark' : 'light';
}

function initialLocale(): Locale {
  if (!browser) return 'tr';
  const stored = localStorage.getItem(LOCALE_KEY);
  return stored === 'en' ? 'en' : 'tr';
}

/** Reactive preferences store, shared across the whole app via module state. */
export const preferences = $state({
  theme: initialTheme(),
  locale: initialLocale(),
});

/** Switches between light and dark theme and persists the choice. */
export function toggleTheme(): void {
  preferences.theme = preferences.theme === 'dark' ? 'light' : 'dark';
  if (browser) localStorage.setItem(THEME_KEY, preferences.theme);
}

/** Switches between Turkish and English UI copy and persists the choice. */
export function toggleLocale(): void {
  preferences.locale = preferences.locale === 'tr' ? 'en' : 'tr';
  if (browser) localStorage.setItem(LOCALE_KEY, preferences.locale);
}
