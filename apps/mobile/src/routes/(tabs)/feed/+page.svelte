<!--
  @component SearchPage
  @desc Search and filtering screen matching UI mockup Image 7. Free-text
    search plus the category/price/date filters picked on /feed/filters
    actually narrow the shared mock event catalogue (§1.4) client-side.
  Props: None
  Events: None
-->
<script lang="ts">
  import { page } from '$app/state';
  import { Search, SlidersHorizontal, Heart, MapPin, ArrowUpRight } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { events } from '$lib/events.svelte.js';

  let searchQuery = $state('');

  let activeCategories = $derived(
    (page.url.searchParams.get('category') ?? '').split(',').filter(Boolean),
  );
  let activePrice = $derived(page.url.searchParams.get('price'));
  let activeCity = $derived(page.url.searchParams.get('city'));
  let activeDate = $derived(page.url.searchParams.get('date'));
  let hasActiveFilters = $derived(
    activeCategories.length > 0 ||
      Boolean(activePrice) ||
      Boolean(activeCity) ||
      Boolean(activeDate),
  );

  let results = $derived(
    events.filter((e) => {
      const query = searchQuery.trim().toLowerCase();
      if (query && !`${e.title} ${e.venue}`.toLowerCase().includes(query)) return false;
      if (activeCategories.length > 0 && !activeCategories.includes(e.category)) return false;
      if (activePrice && e.price !== activePrice) return false;
      if (activeCity && e.location !== activeCity) return false;
      if (activeDate && e.date !== activeDate) return false;
      return true;
    }),
  );

  let topResult = $derived(results.find((e) => e.popular) ?? results[0]);
  let restResults = $derived(results.filter((e) => e.id !== topResult?.id));

  // Frontend-only favorite toggle (no backend sync).
  let favorites = $state(new Set<string>());

  function toggleFavorite(id: string) {
    if (favorites.has(id)) favorites.delete(id);
    else favorites.add(id);
    favorites = new Set(favorites);
  }
</script>

<div class="px-5 py-4 space-y-5 max-w-sm mx-auto">
  <!-- Header: Ara & Brand -->
  <div class="flex items-center justify-between pt-1">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">{t('feed.title')}</h1>
    <span class="text-xl font-black text-[#ea580c] tracking-tight">Keşfet.</span>
  </div>

  <!-- Search Input + Orange Filter Button (Mockup 7) -->
  <div class="flex items-center gap-2.5">
    <div class="relative flex-1">
      <input
        type="text"
        bind:value={searchQuery}
        placeholder={t('feed.search_placeholder')}
        class="w-full h-12 pl-4 pr-10 rounded-2xl border border-border/80 bg-white dark:bg-card text-sm placeholder:text-muted-foreground/60 shadow-xs focus:outline-none focus:ring-2 focus:ring-[#ea580c]/30 focus:border-[#ea580c] transition-all"
      />
      <div
        class="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"
      >
        <Search class="w-4 h-4" />
      </div>
    </div>

    <a
      href="/feed/filters"
      class="relative h-12 px-4 rounded-2xl bg-[#ea580c] hover:bg-[#c2410c] text-white text-xs font-semibold flex items-center gap-1.5 shadow-xs transition-colors shrink-0"
    >
      <SlidersHorizontal class="w-3.5 h-3.5" />
      <span>{t('feed.filter')}</span>
      {#if hasActiveFilters}
        <span
          class="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-[#ef4444] border-2 border-white"
        ></span>
      {/if}
    </a>
  </div>

  {#if results.length === 0}
    <p class="text-sm text-muted-foreground text-center py-10">{t('discover.no_results')}</p>
  {/if}

  {#if topResult}
    <!-- Featured Result -->
    <div class="space-y-3 pt-2">
      <h2 class="text-lg font-bold text-foreground">{t('feed.popular_events')}</h2>

      <div class="relative rounded-3xl overflow-hidden shadow-md group">
        <a href="/events/{topResult.id}" class="block relative aspect-[4/3] w-full">
          <img
            src={topResult.image}
            alt={topResult.title}
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
          <div
            class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-black/20"
          ></div>

          <!-- Badges -->
          <div class="absolute top-4 left-4 right-4 flex items-center justify-between">
            <span
              class="px-3 py-1 rounded-xl bg-[#ef4444] text-white font-bold text-[11px] tracking-wider uppercase shadow-xs"
            >
              {t('common.popular_badge')}
            </span>
            <button
              type="button"
              aria-label={t('common.like')}
              class="w-9 h-9 rounded-full bg-white/90 backdrop-blur-xs flex items-center justify-center text-[#ef4444] shadow-xs hover:bg-white transition-colors cursor-pointer"
              onclick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                toggleFavorite(topResult.id);
              }}
            >
              <Heart class="w-4 h-4 {favorites.has(topResult.id) ? 'fill-current' : ''}" />
            </button>
          </div>

          <!-- Info -->
          <div class="absolute bottom-4 left-4 right-4 flex items-end justify-between">
            <div class="space-y-1 text-white pr-2">
              <h3 class="text-lg font-bold tracking-tight leading-tight drop-shadow-sm">
                {topResult.title}
              </h3>
              <div class="flex items-center gap-1.5 text-xs text-white/90">
                <MapPin class="w-3.5 h-3.5 text-white/80" />
                <span>{topResult.venue}</span>
              </div>
            </div>

            <div
              class="w-11 h-11 rounded-full bg-[#ea580c] flex items-center justify-center text-white shadow-md group-hover:bg-[#c2410c] transition-colors shrink-0"
            >
              <ArrowUpRight class="w-5 h-5 stroke-[2.5]" />
            </div>
          </div>
        </a>
      </div>
    </div>
  {/if}

  {#if restResults.length > 0}
    <div class="space-y-3 pt-2">
      <h2 class="text-lg font-bold text-foreground">{t('feed.recent')}</h2>
      <div class="space-y-2.5">
        {#each restResults as item (item.id)}
          <a
            href="/events/{item.id}"
            class="flex items-center justify-between p-3 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-[#ea580c]/30 hover:shadow-sm transition-all"
          >
            <div class="flex items-center gap-3">
              <img
                src={item.image}
                alt={item.title}
                class="w-14 h-14 rounded-xl object-cover shrink-0"
              />
              <div class="space-y-0.5">
                <h3 class="text-sm font-bold text-foreground leading-snug line-clamp-1">
                  {item.title}
                </h3>
                <p class="text-xs text-muted-foreground">{item.date} • {item.time}</p>
              </div>
            </div>
            <button
              type="button"
              aria-label={t('common.favorite')}
              class="p-2 transition-colors cursor-pointer {favorites.has(item.id)
                ? 'text-[#ef4444]'
                : 'text-muted-foreground hover:text-[#ef4444]'}"
              onclick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                toggleFavorite(item.id);
              }}
            >
              <Heart class="w-4 h-4 {favorites.has(item.id) ? 'fill-current' : ''}" />
            </button>
          </a>
        {/each}
      </div>
    </div>
  {/if}
</div>
