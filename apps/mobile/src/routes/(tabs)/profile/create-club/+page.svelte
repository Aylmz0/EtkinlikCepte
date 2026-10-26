<!--
  @component CreateClubPage
  @desc Form to publish a new club/venue into the shared mock catalogue
    (§1.4). Frontend-only: the created club is added to local app state (and
    shows up immediately in Mekanlar), it is not sent to a backend.
  Props: None
  Events: None
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { ArrowLeft, ImagePlus, Check } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { addClub, type ClubCategoryKey } from '$lib/clubs.svelte.js';
  import type { EventLocation } from '$lib/events.svelte.js';
  import { TURKISH_CITIES } from '$lib/turkishCities.js';

  const FALLBACK_IMAGE =
    'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80';

  let imagePreview = $state<string | undefined>(undefined);
  let fileInput: HTMLInputElement;

  function onImageChange(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    imagePreview = URL.createObjectURL(file);
  }

  let name = $state('');
  let address = $state('');
  let location = $state<EventLocation>('İstanbul');
  let categoryKey = $state<ClubCategoryKey>('clubs.category_concert_hall');
  let description = $state('');

  const locations = TURKISH_CITIES;
  const categories: { id: ClubCategoryKey }[] = [
    { id: 'clubs.category_concert_hall' },
    { id: 'clubs.category_outdoor_theater' },
    { id: 'clubs.category_park_stage' },
    { id: 'clubs.category_culture_art' },
  ];

  let canSubmit = $derived(name.trim() !== '' && address.trim() !== '');

  function submit(e: Event) {
    e.preventDefault();
    if (!canSubmit) return;
    const created = addClub({
      title: name.trim(),
      address: address.trim(),
      location,
      categoryKey,
      description: description.trim() || t('clubDetail.about'),
      image: imagePreview ?? FALLBACK_IMAGE,
    });
    goto(`/clubs/${created.id}`);
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
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('createClub.title')}</h1>
  </div>

  <form class="space-y-6" onsubmit={submit}>
    <div class="space-y-1.5">
      <span class="text-xs font-medium text-foreground/80">{t('createClub.image_label')}</span>
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
            <span class="text-xs">{t('createClub.image_label')}</span>
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
      <label for="cc-name" class="text-xs font-medium text-foreground/80"
        >{t('createClub.name_label')}</label
      >
      <input
        id="cc-name"
        type="text"
        bind:value={name}
        placeholder={t('createClub.name_placeholder')}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <label for="cc-address" class="text-xs font-medium text-foreground/80"
        >{t('createClub.address_label')}</label
      >
      <input
        id="cc-address"
        type="text"
        bind:value={address}
        placeholder={t('createClub.address_placeholder')}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <label for="cc-location" class="text-xs font-medium text-foreground/80"
        >{t('createClub.location_label')}</label
      >
      <select
        id="cc-location"
        bind:value={location}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      >
        {#each locations as loc}
          <option value={loc}>{loc}</option>
        {/each}
      </select>
    </div>

    <div class="space-y-1.5">
      <span class="text-xs font-medium text-foreground/80">{t('createClub.category_label')}</span>
      <div class="grid grid-cols-2 gap-2.5">
        {#each categories as option (option.id)}
          {@const active = categoryKey === option.id}
          <button
            type="button"
            onclick={() => (categoryKey = option.id)}
            class="flex items-center justify-between px-4 py-3 rounded-2xl border text-sm font-semibold transition-all cursor-pointer {active
              ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
              : 'bg-white dark:bg-card border-border/80 text-foreground hover:border-[#ea580c]/30'}"
          >
            <span>{t(option.id)}</span>
            {#if active}<Check class="w-4 h-4" />{/if}
          </button>
        {/each}
      </div>
    </div>

    <div class="space-y-1.5">
      <label for="cc-description" class="text-xs font-medium text-foreground/80"
        >{t('createClub.description_label')}</label
      >
      <textarea
        id="cc-description"
        rows="4"
        bind:value={description}
        placeholder={t('createClub.description_placeholder')}
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
      {t('createClub.submit')}
    </button>
  </form>
</div>
