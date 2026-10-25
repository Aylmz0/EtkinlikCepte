/**
 * Reactive, localStorage-backed chat appearance preferences (background,
 * font size, disappearing messages). Frontend-only: no backend sync.
 * Shared between the chat settings screen and the chat thread screens so a
 * change is visible immediately.
 */
import { browser } from '$app/environment';

export type ChatBackground = 'default' | 'mint' | 'sunset' | 'midnight';
export type ChatFontSize = 'sm' | 'md' | 'lg';

const BG_KEY = 'ec-chat-bg';
const FONT_KEY = 'ec-chat-font';
const DISAPPEARING_KEY = 'ec-chat-disappearing';

/** Tailwind classes for each wallpaper option, shared by the picker swatches
 * and the live chat thread background. "default" is intentionally empty —
 * a background class on the thread element only ever covers that element's
 * own (content-sized) box, so it can never pixel-match the full-page canvas
 * gradient behind it; leaving it transparent lets the real page background
 * show through with no seam instead of trying to re-paint a shorter copy of it. */
export const CHAT_BACKGROUND_CLASSES: Record<ChatBackground, string> = {
  default: '',
  mint: 'bg-gradient-to-b from-[#ecfdf5] to-[#d1fae5] dark:from-[#0d1f18] dark:to-[#102a20]',
  sunset: 'bg-gradient-to-b from-[#fff2e6] to-[#fed7aa]/50 dark:from-[#2a1b10] dark:to-[#3a2415]',
  midnight: 'bg-gradient-to-b from-[#1e293b] to-[#0f172a] text-white',
};

/** Tailwind text-size class for each font-size option. */
export const CHAT_FONT_SIZE_CLASSES: Record<ChatFontSize, string> = {
  sm: 'text-[11px]',
  md: 'text-xs',
  lg: 'text-sm',
};

function readBackground(): ChatBackground {
  if (!browser) return 'default';
  const v = localStorage.getItem(BG_KEY);
  return v === 'mint' || v === 'sunset' || v === 'midnight' ? v : 'default';
}

function readFontSize(): ChatFontSize {
  if (!browser) return 'md';
  const v = localStorage.getItem(FONT_KEY);
  return v === 'sm' || v === 'lg' ? v : 'md';
}

function readDisappearing(): boolean {
  if (!browser) return false;
  return localStorage.getItem(DISAPPEARING_KEY) === '1';
}

/** Reactive chat settings store, shared across the whole app via module state. */
export const chatSettings = $state({
  background: readBackground(),
  fontSize: readFontSize(),
  disappearing: readDisappearing(),
});

/** Updates the chat wallpaper and persists it. */
export function setChatBackground(background: ChatBackground): void {
  chatSettings.background = background;
  if (browser) localStorage.setItem(BG_KEY, background);
}

/** Updates the chat bubble text size and persists it. */
export function setChatFontSize(size: ChatFontSize): void {
  chatSettings.fontSize = size;
  if (browser) localStorage.setItem(FONT_KEY, size);
}

/** Toggles the disappearing-messages preference and persists it. */
export function toggleDisappearing(): void {
  chatSettings.disappearing = !chatSettings.disappearing;
  if (browser) localStorage.setItem(DISAPPEARING_KEY, chatSettings.disappearing ? '1' : '0');
}
