<!--
  @component DiscoverPage
  @desc Main event discovery screen matching UI mockup Image 6. The quick
    filters (tonight/weekend/this week/date) and the location picker actually
    narrow the shared mock event catalogue (§1.4) client-side.
  Props: None
  Events: None
-->
<script lang="ts">
  import {
    MapPin,
    ChevronDown,
    Moon,
    Sparkles,
    Clock,
    Calendar,
    Heart,
    ArrowUpRight,
    ArrowRight,
  } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { preferences } from '$lib/preferences.svelte.js';
  import { Calendar as CalendarPicker, clickOutside } from '@etkinlikcepte/ui';
  import {
    events,
    isToday,
    isThisWeek,
    isThisWeekend,
    type EventLocation,
  } from '$lib/events.svelte.js';
  import { TURKISH_CITIES } from '$lib/turkishCities.js';

  const filterChips = [
    { id: 'tonight', labelKey: 'discover.filter_tonight', icon: Moon },
    { id: 'weekend', labelKey: 'discover.filter_weekend', icon: Sparkles },
    { id: 'week', labelKey: 'discover.filter_this_week', icon: Clock },
    { id: 'date', labelKey: 'discover.filter_pick_date', icon: Calendar },
  ];

  // Frontend-only filter selection (no backend query wired yet).
  let selectedFilter = $state('tonight');
  let pickedDate = $state<string | undefined>(undefined);
  let datePickerOpen = $state(false);
  let intlLocale = $derived(preferences.locale === 'tr' ? 'tr-TR' : 'en-US');

  function selectChip(id: string) {
    if (id === 'date') {
      datePickerOpen = !datePickerOpen;
      return;
    }
    datePickerOpen = false;
    selectedFilter = id;
  }

  function closeDatePicker() {
    datePickerOpen = false;
    selectedFilter = pickedDate ? 'date' : 'tonight';
  }

  let selectedLocation = $state<EventLocation>('İstanbul');
  let locationMenuOpen = $state(false);
  let citySearch = $state('');
  let filteredCities = $derived(
    TURKISH_CITIES.filter((city) =>
      city.toLocaleLowerCase('tr').includes(citySearch.toLocaleLowerCase('tr')),
    ),
  );

  function pickLocation(name: EventLocation) {
    selectedLocation = name;
    locationMenuOpen = false;
    citySearch = '';
  }

  let filteredEvents = $derived(
    events.filter((e) => {
      if (e.location !== selectedLocation) return false;
      if (selectedFilter === 'tonight') return isToday(e.date);
      if (selectedFilter === 'weekend') return isThisWeekend(e.date);
      if (selectedFilter === 'week') return isThisWeek(e.date);
      if (selectedFilter === 'date') return pickedDate ? e.date === pickedDate : true;
      return true;
    }),
  );
  let heroEvent = $derived(filteredEvents.find((e) => e.popular) ?? filteredEvents[0]);
  let listEvents = $derived(filteredEvents.filter((e) => e.id !== heroEvent?.id));

  // Frontend-only favorite toggle (no backend sync).
  let favorites = $state(new Set<string>());

  function toggleFavorite(id: string) {
    if (favorites.has(id)) favorites.delete(id);
    else favorites.add(id);
    favorites = new Set(favorites);
  }
</script>

<div class="px-5 py-4 space-y-6 max-w-sm mx-auto">
  <!-- Top Header with Brand & Location Picker -->
  <div class="flex items-center justify-between">
    <span class="text-xl font-black text-[#ea580c] tracking-tight">Keşfet.</span>
    <div class="relative" use:clickOutside={() => (locationMenuOpen = false)}>
      <button
        type="button"
        onclick={() => (locationMenuOpen = !locationMenuOpen)}
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white dark:bg-card border border-border/80 text-xs font-medium text-foreground shadow-xs hover:bg-muted/40 transition-colors cursor-pointer"
      >
        <MapPin class="w-3.5 h-3.5 text-[#ea580c]" />
        <span>{selectedLocation}</span>
        <ChevronDown
          class="w-3 h-3 text-muted-foreground transition-transform {locationMenuOpen
            ? 'rotate-180'
            : ''}"
        />
      </button>
      {#if locationMenuOpen}
        <div
          class="absolute right-0 top-full mt-2 w-48 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-lg p-1.5 z-20"
        >
          <input
            type="text"
            bind:value={citySearch}
            placeholder={t('discover.city_search_placeholder')}
            class="w-full h-9 px-3 mb-1.5 rounded-xl border border-border/80 bg-background text-xs placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-[#ea580c]/30 focus:border-[#ea580c] transition-all"
          />
          <div class="max-h-56 overflow-y-auto">
            {#each filteredCities as name (name)}
              <button
                type="button"
                onclick={() => pickLocation(name)}
                class="w-full px-3.5 py-2 text-left text-xs font-medium rounded-lg transition-colors cursor-pointer {selectedLocation ===
                name
                  ? 'text-[#ea580c] font-semibold'
                  : 'text-foreground hover:bg-muted/40'}"
              >
                {name}
              </button>
            {:else}
              <p class="px-3.5 py-2 text-xs text-muted-foreground">{t('discover.no_results')}</p>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Page Headline -->
  <div>
    <h1 class="text-2xl font-extrabold tracking-tight text-foreground leading-snug">
      {t('discover.headline')}
    </h1>
  </div>

  <!-- Filter Chips Row (Mockup 6) -->
  <div class="grid grid-cols-4 gap-2">
    {#each filterChips as chip}
      {@const Icon = chip.icon}
      {@const active = selectedFilter === chip.id}
      <div
        class="relative"
        use:clickOutside={() => {
          if (chip.id === 'date') closeDatePicker();
        }}
      >
        <button
          type="button"
          onclick={() => selectChip(chip.id)}
          class="w-full flex flex-col items-center justify-center p-2.5 rounded-2xl border text-center transition-all cursor-pointer {active
            ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c] shadow-xs'
            : 'bg-white dark:bg-card border-border/80 text-muted-foreground hover:border-[#ea580c]/30'}"
        >
          <Icon class="w-4 h-4 mb-1.5 {active ? 'text-[#ea580c]' : 'text-foreground/70'}" />
          <span class="text-[11px] font-semibold leading-tight">
            {chip.id === 'date' && pickedDate ? pickedDate : t(chip.labelKey)}
          </span>
        </button>
        {#if chip.id === 'date' && datePickerOpen}
          <div class="absolute left-1/2 -translate-x-1/2 top-full mt-2 z-30">
            <CalendarPicker
              bind:value={pickedDate}
              locale={intlLocale}
              todayLabel={t('common.today')}
              clearLabel={t('filters.clear')}
              onClose={closeDatePicker}
            />
          </div>
        {/if}
      </div>
    {/each}
  </div>

  {#if heroEvent}
    <!-- Featured Event Hero Card (Mockup 6) -->
    <div class="relative rounded-3xl overflow-hidden shadow-md group">
      <a href="/events/{heroEvent.id}" class="block relative aspect-[4/3] w-full">
        <!-- Background Image -->
        <img
          src={heroEvent.image}
          alt={heroEvent.title}
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-black/20"></div>

        <!-- Top Badges -->
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
              toggleFavorite(heroEvent.id);
            }}
          >
            <Heart class="w-4 h-4 {favorites.has(heroEvent.id) ? 'fill-current' : ''}" />
          </button>
        </div>

        <!-- Bottom Card Info -->
        <div class="absolute bottom-4 left-4 right-4 flex items-end justify-between">
          <div class="space-y-1 text-white pr-2">
            <h2 class="text-xl font-bold tracking-tight leading-tight drop-shadow-sm">
              {heroEvent.title}
            </h2>
            <div class="flex items-center gap-1.5 text-xs text-white/90">
              <MapPin class="w-3.5 h-3.5 text-white/80" />
              <span>{heroEvent.venue}</span>
            </div>
            <div class="flex items-center gap-1.5 text-xs text-white/80">
              <Calendar class="w-3.5 h-3.5 text-white/80" />
              <span>{heroEvent.date} • {heroEvent.time}</span>
            </div>
          </div>

          <!-- Orange Arrow Button -->
          <div
            class="w-11 h-11 rounded-full bg-[#ea580c] flex items-center justify-center text-white shadow-md group-hover:bg-[#c2410c] transition-colors shrink-0"
          >
            <ArrowUpRight class="w-5 h-5 stroke-[2.5]" />
          </div>
        </div>
      </a>
    </div>
  {:else}
    <p class="text-sm text-muted-foreground text-center py-8">{t('discover.no_results')}</p>
  {/if}

  <!-- Popüler Etkinlikler Section -->
  {#if listEvents.length > 0}
    <div class="space-y-3 pt-1">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-bold text-foreground">{t('discover.popular_events')}</h2>
        <a
          href="/feed"
          aria-label={t('common.view_all')}
          class="w-7 h-7 rounded-full bg-[#ef4444] flex items-center justify-center text-white shadow-xs hover:bg-[#dc2626] transition-colors"
        >
          <ArrowRight class="w-3.5 h-3.5" />
        </a>
      </div>

      <!-- Event List -->
      <div class="space-y-3">
        {#each listEvents as item (item.id)}
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
