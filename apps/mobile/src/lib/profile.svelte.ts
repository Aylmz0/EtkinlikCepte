/**
 * Reactive, localStorage-backed profile fields (display name, username,
 * bio, city, website, interests). The avatar is an in-memory object URL
 * only — it never outlives the tab, since actual avatar storage is
 * backend-dependent and not wired here.
 *
 * Frontend-only state: no backend call, no account sync.
 */
import { browser } from '$app/environment';
import type { EventCategory, EventLocation } from './events.svelte.js';

const NAME_KEY = 'ec-profile-name';
const USERNAME_KEY = 'ec-profile-username';
const BIO_KEY = 'ec-profile-bio';
const CITY_KEY = 'ec-profile-city';
const WEBSITE_KEY = 'ec-profile-website';
const INTERESTS_KEY = 'ec-profile-interests';

const DEFAULT_NAME = 'Kullanıcı Adı';

function readString(key: string, fallback: string): string {
  if (!browser) return fallback;
  return localStorage.getItem(key) ?? fallback;
}

function readInterests(): EventCategory[] {
  if (!browser) return [];
  try {
    const raw = localStorage.getItem(INTERESTS_KEY);
    return raw ? (JSON.parse(raw) as EventCategory[]) : [];
  } catch {
    return [];
  }
}

/** Reactive profile store, shared across the whole app via module state. */
export const profile = $state({
  name: readString(NAME_KEY, DEFAULT_NAME),
  username: readString(USERNAME_KEY, ''),
  bio: readString(BIO_KEY, ''),
  city: readString(CITY_KEY, '') as EventLocation | '',
  website: readString(WEBSITE_KEY, ''),
  interests: readInterests(),
  avatarUrl: undefined as string | undefined,
});

/** Updates the display name and persists it. */
export function setName(name: string): void {
  profile.name = name;
  if (browser) localStorage.setItem(NAME_KEY, name);
}

/** Updates the @handle and persists it. */
export function setUsername(username: string): void {
  profile.username = username;
  if (browser) localStorage.setItem(USERNAME_KEY, username);
}

/** Updates the bio and persists it. */
export function setBio(bio: string): void {
  profile.bio = bio;
  if (browser) localStorage.setItem(BIO_KEY, bio);
}

/** Updates the home city and persists it. */
export function setCity(city: EventLocation | ''): void {
  profile.city = city;
  if (browser) localStorage.setItem(CITY_KEY, city);
}

/** Updates the website/social link and persists it. */
export function setWebsite(website: string): void {
  profile.website = website;
  if (browser) localStorage.setItem(WEBSITE_KEY, website);
}

/** Replaces the favorite event categories and persists them. */
export function setInterests(interests: EventCategory[]): void {
  profile.interests = interests;
  if (browser) localStorage.setItem(INTERESTS_KEY, JSON.stringify(interests));
}

/** Replaces the locally previewed avatar, releasing the previous object URL. */
export function setAvatar(url: string | undefined): void {
  if (profile.avatarUrl) URL.revokeObjectURL(profile.avatarUrl);
  profile.avatarUrl = url;
}
