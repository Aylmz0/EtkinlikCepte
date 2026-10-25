<!--
  @component FeedFiltersPage
  @desc Search filters for the Ara (feed) screen. Category, price, and date
    actually narrow the shared mock event catalogue (§1.4) — "Uygula" encodes
    the selection into the /feed query string, which the feed page reads.
  Props: None
  Events: None
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/state';
  import { ArrowLeft, Check, Calendar as CalendarIcon, MapPin, ChevronDown } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { preferences } from '$lib/preferences.svelte.js';
  import { Calendar as CalendarPicker, clickOutside } from '@etkinlikcepte/ui';
  import { TURKISH_CITIES } from '$lib/turkishCities.js';

  const categories = [
    { id: 'concert', labelKey: 'filters.category_concert' },
    { id: 'festival', labelKey: 'filters.category_festival' },
    { id: 'sport', labelKey: 'filters.category_sport' },
    { id: 'art', labelKey: 'filters.category_art' },
  ];

  // Pre-fill from the current /feed query string so re-opening Filtreler
  // shows whatever is already applied.
  let selectedCategories = $state(
    new Set((page.url.searchParams.get('category') ?? '').split(',').filter(Boolean)),
  );
  let selectedPrice = $state(page.url.searchParams.get('price') ?? 'any');
  let selectedCity = $state(page.url.searchParams.get('city') ?? '');
  let pickedDate = $state<string | undefined>(page.url.searchParams.get('date') ?? undefined);
  let datePickerOpen = $state(false);
  let cityMenuOpen = $state(false);
  let citySearch = $state('');
  let intlLocale = $derived(preferences.locale === 'tr' ? 'tr-TR' : 'en-US');
  let filteredCities = $derived(
    TURKISH_CITIES.filter((city) =>
      city.toLocaleLowerCase('tr').includes(citySearch.toLocaleLowerCase('tr')),
    ),
  );

  function pickCity(city: string) {
    selectedCity = city;
    cityMenuOpen = false;
    citySearch = '';
  }

  function toggleCategory(id: string) {
    if (selectedCategories.has(id)) selectedCategories.delete(id);
    else selectedCategories.add(id);
    selectedCategories = new Set(selectedCategories);
  }

  const priceOptions = [
    { id: 'any', labelKey: 'filters.price_any' },
    { id: 'free', labelKey: 'filters.price_free' },
    { id: 'paid', labelKey: 'filters.price_paid' },
  ];

  function clearFilters() {
    selectedCategories = new Set();
    selectedPrice = 'any';
    selectedCity = '';
    pickedDate = undefined;
  }

  function applyFilters() {
    const params = new URLSearchParams();
    if (selectedCategories.size > 0) params.set('category', [...selectedCategories].join(','));
    if (selectedPrice !== 'any') params.set('price', selectedPrice);
    if (selectedCity) params.set('city', selectedCity);
    if (pickedDate) params.set('date', pickedDate);
    const query = params.toString();
    goto(query ? `/feed?${query}` : '/feed');
  }
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto space-y-6 pb-12">
  <div class="flex items-center gap-3 pt-2">
    <a
      href="/feed"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('filters.title')}</h1>
  </div>

  <div class="space-y-3">
    <h2 class="text-sm font-bold text-foreground">{t('filters.category')}</h2>
    <div class="grid grid-cols-2 gap-2.5">
      {#each categories as cat (cat.id)}
        {@const active = selectedCategories.has(cat.id)}
        <button
          type="button"
          onclick={() => toggleCategory(cat.id)}
          class="flex items-center justify-between px-4 py-3 rounded-2xl border text-sm font-semibold transition-all cursor-pointer {active
            ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
            : 'bg-white dark:bg-card border-border/80 text-foreground hover:border-[#ea580c]/30'}"
        >
          <span>{t(cat.labelKey)}</span>
          {#if active}<Check class="w-4 h-4" />{/if}
        </button>
      {/each}
    </div>
  </div>

  <div class="space-y-3 relative" use:clickOutside={() => (cityMenuOpen = false)}>
    <h2 class="text-sm font-bold text-foreground">{t('filters.location')}</h2>
    <button
      type="button"
      onclick={() => (cityMenuOpen = !cityMenuOpen)}
      class="w-full flex items-center justify-between px-4 py-3 rounded-2xl border text-sm font-semibold transition-all cursor-pointer {selectedCity
        ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
        : 'bg-white dark:bg-card border-border/80 text-foreground hover:border-[#ea580c]/30'}"
    >
      <span class="flex items-center gap-2">
        <MapPin class="w-4 h-4" />
        {selectedCity || t('filters.location_placeholder')}
      </span>
      <ChevronDown class="w-3.5 h-3.5 transition-transform {cityMenuOpen ? 'rotate-180' : ''}" />
    </button>
    {#if cityMenuOpen}
      <div
        class="absolute left-0 right-0 top-full mt-2 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-lg p-1.5 z-30"
      >
        <input
          type="text"
          bind:value={citySearch}
          placeholder={t('discover.city_search_placeholder')}
          class="w-full h-9 px-3 mb-1.5 rounded-xl border border-border/80 bg-background text-xs placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-[#ea580c]/30 focus:border-[#ea580c] transition-all"
        />
        <div class="max-h-56 overflow-y-auto">
          <button
            type="button"
            onclick={() => pickCity('')}
            class="w-full px-3.5 py-2 text-left text-xs font-medium rounded-lg transition-colors cursor-pointer {selectedCity ===
            ''
              ? 'text-[#ea580c] font-semibold'
              : 'text-foreground hover:bg-muted/40'}"
          >
            {t('filters.location_any')}
          </button>
          {#each filteredCities as city (city)}
            <button
              type="button"
              onclick={() => pickCity(city)}
              class="w-full px-3.5 py-2 text-left text-xs font-medium rounded-lg transition-colors cursor-pointer {selectedCity ===
              city
                ? 'text-[#ea580c] font-semibold'
                : 'text-foreground hover:bg-muted/40'}"
            >
              {city}
            </button>
          {:else}
            <p class="px-3.5 py-2 text-xs text-muted-foreground">{t('discover.no_results')}</p>
          {/each}
        </div>
      </div>
    {/if}
  </div>

  <div class="space-y-3">
    <h2 class="text-sm font-bold text-foreground">{t('filters.price')}</h2>
    <div class="grid grid-cols-3 gap-2.5">
      {#each priceOptions as opt (opt.id)}
        <button
          type="button"
          onclick={() => (selectedPrice = opt.id)}
          class="px-3 py-2.5 rounded-2xl border text-xs font-semibold transition-all cursor-pointer {selectedPrice ===
          opt.id
            ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
            : 'bg-white dark:bg-card border-border/80 text-foreground hover:border-[#ea580c]/30'}"
        >
          {t(opt.labelKey)}
        </button>
      {/each}
    </div>
  </div>

  <div class="space-y-3 relative" use:clickOutside={() => (datePickerOpen = false)}>
    <h2 class="text-sm font-bold text-foreground">{t('filters.date')}</h2>
    <button
      type="button"
      onclick={() => (datePickerOpen = !datePickerOpen)}
      class="w-full flex items-center gap-2.5 px-4 py-3 rounded-2xl border text-sm font-semibold transition-all cursor-pointer {pickedDate
        ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
        : 'bg-white dark:bg-card border-border/80 text-foreground hover:border-[#ea580c]/30'}"
    >
      <CalendarIcon class="w-4 h-4" />
      <span>{pickedDate ?? t('filters.date_placeholder')}</span>
    </button>
    {#if datePickerOpen}
      <div class="absolute left-0 top-full mt-2 z-30">
        <CalendarPicker
          bind:value={pickedDate}
          locale={intlLocale}
          todayLabel={t('common.today')}
          clearLabel={t('filters.clear')}
          onClose={() => (datePickerOpen = false)}
        />
      </div>
    {/if}
  </div>

  <div class="flex gap-3 pt-2">
    <button
      type="button"
      onclick={clearFilters}
      class="flex-1 h-12 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground font-semibold text-sm shadow-xs hover:bg-muted/40 transition-colors cursor-pointer"
    >
      {t('filters.clear')}
    </button>
    <button
      type="button"
      onclick={() => goto('/feed')}
      class="flex-1 h-12 rounded-2xl bg-primary text-primary-foreground font-semibold text-sm shadow-sm hover:bg-[#dc2626] transition-colors cursor-pointer"
    >
      {t('filters.apply')}
    </button>
  </div>
</div>
