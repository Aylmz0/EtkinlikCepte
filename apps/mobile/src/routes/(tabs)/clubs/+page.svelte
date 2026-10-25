<!--
  @component VenuesPage
  @desc Venues screen matching UI mockup Image 9.
  Props: None
  Events: None
-->
<script lang="ts">
  import { MapPin, Search, Star, Heart } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { clubs as venues } from '$lib/clubs.svelte.js';

  // Frontend-only favorite toggle (no backend sync).
  let favorites = $state(new Set<string>());

  function toggleFavorite(id: string) {
    if (favorites.has(id)) favorites.delete(id);
    else favorites.add(id);
    favorites = new Set(favorites);
  }
</script>

<div class="px-5 py-4 space-y-5 max-w-sm mx-auto">
  <!-- Title and Subtitle -->
  <div class="space-y-1 pt-1">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">{t('clubs.title')}</h1>
    <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
      <MapPin class="w-3.5 h-3.5 text-[#ef4444]" />
      <span>{t('clubs.nearby')}</span>
    </div>
  </div>

  <!-- Search Input Bar -->
  <div class="relative">
    <div class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none">
      <Search class="w-4 h-4" />
    </div>
    <input
      type="text"
      placeholder={t('clubs.search_placeholder')}
      class="w-full h-12 pl-11 pr-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-sm placeholder:text-muted-foreground/60 shadow-xs focus:outline-none focus:ring-2 focus:ring-[#ea580c]/30 focus:border-[#ea580c] transition-all"
    />
  </div>

  <!-- Section Header -->
  <div class="flex items-center justify-between pt-1">
    <h2 class="text-lg font-bold text-foreground">{t('clubs.featured')}</h2>
    <span class="text-xs text-muted-foreground">{venues.length} {t('clubs.count_suffix')}</span>
  </div>

  <!-- Venues List (Mockup 9) -->
  <div class="space-y-3">
    {#each venues as venue}
      <a
        href="/clubs/{venue.id}"
        class="flex items-center justify-between p-3.5 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-[#ea580c]/40 hover:shadow-sm transition-all"
      >
        <div class="flex items-center gap-3.5">
          <img
            src={venue.image}
            alt={venue.title}
            class="w-18 h-18 rounded-2xl object-cover shrink-0"
          />
          <div class="space-y-1">
            <h3 class="text-sm font-bold text-foreground leading-snug line-clamp-1">
              {venue.title}
            </h3>
            <p class="text-xs text-muted-foreground">{venue.address}</p>
            <div class="flex items-center gap-1.5 text-xs font-semibold text-foreground">
              {#if venue.rating}
                <Star class="w-3 h-3 text-[#ef4444] fill-current" />
                <span>{venue.rating}</span>
                <span class="text-muted-foreground/40">•</span>
              {/if}
              <span class="text-foreground">{t('clubs.status_open')}</span>
            </div>
            <p class="text-[11px] text-muted-foreground/80">{t(venue.categoryKey)}</p>
          </div>
        </div>

        <button
          type="button"
          aria-label={t('clubs.add_favorite')}
          class="p-2 transition-colors cursor-pointer self-center {favorites.has(venue.id)
            ? 'text-[#ef4444]'
            : 'text-muted-foreground hover:text-[#ef4444]'}"
          onclick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            toggleFavorite(venue.id);
          }}
        >
          <Heart class="w-4 h-4 {favorites.has(venue.id) ? 'fill-current' : ''}" />
        </button>
      </a>
    {/each}
  </div>
</div>
