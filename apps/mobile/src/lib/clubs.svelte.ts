/**
 * Shared mock club/venue catalogue used by Mekanlar and the club detail
 * screens until the real clubs API lands (§1.4). Reactive ($state) so a
 * club created on /profile/create-club shows up immediately.
 */
import { browser } from '$app/environment';
import { SvelteSet } from 'svelte/reactivity';
import type { EventLocation } from './events.svelte.js';

export type ClubCategoryKey =
  | 'clubs.category_outdoor_theater'
  | 'clubs.category_concert_hall'
  | 'clubs.category_park_stage'
  | 'clubs.category_culture_art';

export interface Club {
  id: string;
  title: string;
  address: string;
  location: EventLocation;
  categoryKey: ClubCategoryKey;
  description: string;
  image: string;
  /** Average rating as a display string (e.g. "4.8"); absent for new, unrated clubs. */
  rating?: string;
}

const DEFAULT_DESCRIPTION =
  'Bu mekan, takip edenlerinin akışında görünen etkinliklere ev sahipliği yapar.';

export const clubs = $state<Club[]>([
  {
    id: 'ohrid-theater',
    title: 'Ancient Theater of Ohrid',
    address: 'Ilindenska • Ohrid',
    location: 'İzmir',
    categoryKey: 'clubs.category_outdoor_theater',
    description: DEFAULT_DESCRIPTION,
    rating: '4.8',
    image:
      'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 'rakometno',
    title: 'Rakometno Igralishte',
    address: 'Bulevar 1-vi Maj • Bitola',
    location: 'İstanbul',
    categoryKey: 'clubs.category_concert_hall',
    description:
      "Konser alanı olarak Bitola'daki en popüler etkinliklere ev sahipliği yapar. Takip ettiğiniz etkinlikler akışınızda görünür.",
    rating: '4.7',
    image:
      'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 'skopje-park',
    title: 'Skopje City Park Stage',
    address: 'Gradski Park • Üsküp',
    location: 'Ankara',
    categoryKey: 'clubs.category_park_stage',
    description: DEFAULT_DESCRIPTION,
    rating: '4.9',
    image:
      'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=400&q=80',
  },
  {
    id: 'mkc',
    title: 'MKC Kültür Merkezi',
    address: 'Kej Dimitar Vlahov • Üsküp',
    location: 'Ankara',
    categoryKey: 'clubs.category_culture_art',
    description: DEFAULT_DESCRIPTION,
    rating: '4.8',
    image:
      'https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=400&q=80',
  },
]);

function slugify(title: string): string {
  return title
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

/**
 * Adds a user-created club to the shared catalogue (frontend-only — not
 * sent to a backend). Returns the created club so the caller can navigate
 * to its detail page.
 *
 * @param input Club fields without `id`/`rating`, which are derived or
 *   left unset here (a new club has no reviews yet).
 */
export function addClub(input: Omit<Club, 'id' | 'rating'>): Club {
  const base = slugify(input.title) || 'kulup';
  let id = base;
  let suffix = 1;
  while (clubs.some((c) => c.id === id)) {
    id = `${base}-${++suffix}`;
  }
  const created: Club = { ...input, id };
  clubs.push(created);
  return created;
}

const FOLLOWED_KEY = 'ec-followed-clubs';

function readFollowed(): string[] {
  if (!browser) return [];
  try {
    const raw = localStorage.getItem(FOLLOWED_KEY);
    return raw ? (JSON.parse(raw) as string[]) : ['rakometno', 'mkc'];
  } catch {
    return [];
  }
}

/** Reactive set of followed club ids, shared across the whole app. `SvelteSet`
 * (not a plain `Set` wrapped in `$state`) is required here — plain `$state`
 * only tracks property assignment, not `Set.add`/`.delete` calls, so a bare
 * `$state(new Set())` silently fails to re-render on follow/unfollow. */
export const followedClubIds = new SvelteSet<string>(readFollowed());

/** Whether the given club is currently followed. */
export function isFollowed(id: string): boolean {
  return followedClubIds.has(id);
}

/** Toggles follow status for a club and persists it. */
export function toggleFollow(id: string): void {
  if (followedClubIds.has(id)) followedClubIds.delete(id);
  else followedClubIds.add(id);
  if (browser) localStorage.setItem(FOLLOWED_KEY, JSON.stringify([...followedClubIds]));
}
