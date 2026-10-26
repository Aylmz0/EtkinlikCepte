<!--
  @component CreateEventPage
  @desc Form to publish a new event into the shared mock catalogue (§1.4).
    Frontend-only: the created event is added to local app state (and shows
    up immediately in Discover/Ara), it is not sent to a backend.
  Props: None
  Events: None
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { ArrowLeft, ImagePlus, Check } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { preferences } from '$lib/preferences.svelte.js';
  import { Calendar as CalendarPicker, clickOutside } from '@etkinlikcepte/ui';
  import {
    addEvent,
    type EventCategory,
    type EventLocation,
    type EventPrice,
  } from '$lib/events.svelte.js';
  import { TURKISH_CITIES } from '$lib/turkishCities.js';

  const FALLBACK_IMAGE =
    'https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80';

  let imagePreview = $state<string | undefined>(undefined);
  let fileInput: HTMLInputElement;

  function onImageChange(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    imagePreview = URL.createObjectURL(file);
  }

  let name = $state('');
  let venue = $state('');
  let location = $state<EventLocation>('İstanbul');
  let category = $state<EventCategory>('concert');
  let price = $state<EventPrice>('free');
  let description = $state('');
  let time = $state('20:00');

  let pickedDate = $state<string | undefined>(undefined);
  let datePickerOpen = $state(false);
  let intlLocale = $derived(preferences.locale === 'tr' ? 'tr-TR' : 'en-US');

  const locations = TURKISH_CITIES;
  const categories: { id: EventCategory; labelKey: string }[] = [
    { id: 'concert', labelKey: 'filters.category_concert' },
    { id: 'festival', labelKey: 'filters.category_festival' },
    { id: 'sport', labelKey: 'filters.category_sport' },
    { id: 'art', labelKey: 'filters.category_art' },
  ];
  const prices: { id: EventPrice; labelKey: string }[] = [
    { id: 'free', labelKey: 'filters.price_free' },
    { id: 'paid', labelKey: 'filters.price_paid' },
  ];

  let canSubmit = $derived(name.trim() !== '' && venue.trim() !== '' && Boolean(pickedDate));

  function submit(e: Event) {
    e.preventDefault();
    if (!canSubmit || !pickedDate) return;
    const created = addEvent({
      title: name.trim(),
      venue: venue.trim(),
      location,
      category,
      price,
      date: pickedDate,
      time,
      image: imagePreview ?? FALLBACK_IMAGE,
      description: description.trim() || t('eventDetail.about'),
    });
    goto(`/events/${created.id}`);
  }
</script>

<div class="min-h-screen px-6 py-8 max-w-sm mx-auto space-y-8 pb-12">
  <div class="flex items-center gap-3">
    <a
      href="/profile"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('createEvent.title')}</h1>
  </div>

  <form class="space-y-6" onsubmit={submit}>
    <div class="space-y-1.5">
      <span class="text-xs font-medium text-foreground/80">{t('createEvent.image_label')}</span>
      <button
        type="button"
        onclick={() => fileInput.click()}
        class="w-full aspect-[4/2.2] rounded-2xl border border-dashed border-border/80 bg-white dark:bg-card overflow-hidden flex items-center justify-center text-muted-foreground/60 cursor-pointer"
      >
        {#if imagePreview}
          <img src={imagePreview} alt="" class="w-full h-full object-cover" />
        {:else}
          <div class="flex flex-col items-center gap-1.5">
            <ImagePlus class="w-5 h-5" />
            <span class="text-xs">{t('createEvent.image_label')}</span>
          </div>
        {/if}
      </button>
      <input
        bind:this={fileInput}
        onchange={onImageChange}
        type="file"
        accept="image/*"
        class="hidden"
      />
    </div>

    <div class="space-y-1.5">
      <label for="ce-name" class="text-xs font-medium text-foreground/80"
        >{t('createEvent.name_label')}</label
      >
      <input
        id="ce-name"
        type="text"
        bind:value={name}
        placeholder={t('createEvent.name_placeholder')}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <label for="ce-venue" class="text-xs font-medium text-foreground/80"
        >{t('createEvent.venue_label')}</label
      >
      <input
        id="ce-venue"
        type="text"
        bind:value={venue}
        placeholder={t('createEvent.venue_placeholder')}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <label for="ce-location" class="text-xs font-medium text-foreground/80"
        >{t('createEvent.location_label')}</label
      >
      <select
        id="ce-location"
        bind:value={location}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      >
        {#each locations as loc}
          <option value={loc}>{loc}</option>
        {/each}
      </select>
    </div>

    <div class="space-y-1.5">
      <span class="text-xs font-medium text-foreground/80">{t('createEvent.category_label')}</span>
      <div class="grid grid-cols-2 gap-2.5">
        {#each categories as option (option.id)}
          {@const active = category === option.id}
          <button
            type="button"
            onclick={() => (category = option.id)}
            class="flex items-center justify-between px-4 py-3 rounded-2xl border text-sm font-semibold transition-all cursor-pointer {active
              ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
              : 'bg-white dark:bg-card border-border/80 text-foreground hover:border-[#ea580c]/30'}"
          >
            <span>{t(option.labelKey)}</span>
            {#if active}<Check class="w-4 h-4" />{/if}
          </button>
        {/each}
      </div>
    </div>

    <div class="space-y-1.5">
      <span class="text-xs font-medium text-foreground/80">{t('createEvent.price_label')}</span>
      <div class="grid grid-cols-2 gap-2.5">
        {#each prices as option (option.id)}
          {@const active = price === option.id}
          <button
            type="button"
            onclick={() => (price = option.id)}
            class="px-3 py-2.5 rounded-2xl border text-xs font-semibold transition-all cursor-pointer {active
              ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
              : 'bg-white dark:bg-card border-border/80 text-foreground hover:border-[#ea580c]/30'}"
          >
            {t(option.labelKey)}
          </button>
        {/each}
      </div>
    </div>

    <div class="grid grid-cols-2 gap-3">
      <div class="space-y-1.5 relative" use:clickOutside={() => (datePickerOpen = false)}>
        <span class="text-xs font-medium text-foreground/80">{t('createEvent.date_label')}</span>
        <button
          type="button"
          onclick={() => (datePickerOpen = !datePickerOpen)}
          class="w-full h-12 px-4 rounded-2xl border text-left text-sm font-medium transition-all cursor-pointer {pickedDate
            ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
            : 'bg-white dark:bg-card border-border/80 text-muted-foreground hover:border-[#ea580c]/30'}"
        >
          {pickedDate ?? t('filters.date_placeholder')}
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

      <div class="space-y-1.5">
        <label for="ce-time" class="text-xs font-medium text-foreground/80"
          >{t('createEvent.time_label')}</label
        >
        <input
          id="ce-time"
          type="time"
          bind:value={time}
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>
    </div>

    <div class="space-y-1.5">
      <label for="ce-description" class="text-xs font-medium text-foreground/80"
        >{t('createEvent.description_label')}</label
      >
      <textarea
        id="ce-description"
        rows="4"
        bind:value={description}
        placeholder={t('createEvent.description_placeholder')}
        class="w-full px-4 py-3 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all resize-none"
      ></textarea>
    </div>

    <button
      type="submit"
      disabled={!canSubmit}
      class="w-full h-12 rounded-2xl font-semibold text-sm shadow-sm transition-all {canSubmit
        ? 'bg-primary text-primary-foreground hover:bg-[#dc2626] active:scale-[0.99] cursor-pointer'
        : 'bg-primary/40 text-primary-foreground cursor-not-allowed'}"
    >
      {t('createEvent.submit')}
    </button>
  </form>
</div>
