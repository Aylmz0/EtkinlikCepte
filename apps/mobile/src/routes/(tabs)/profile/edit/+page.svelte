<!--
  @component ProfileEditPage
  @desc Edit the shared profile fields (name, username, bio, city, website,
    interests, avatar) used across the app (§1.6). Frontend-only: persisted
    to localStorage, not synced to a backend account.
  Props: None
  Events: None
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { ArrowLeft, Camera, Check } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import {
    profile,
    setName,
    setUsername,
    setBio,
    setCity,
    setWebsite,
    setInterests,
    setAvatar,
  } from '$lib/profile.svelte.js';
  import type { EventCategory } from '$lib/events.svelte.js';
  import { TURKISH_CITIES } from '$lib/turkishCities.js';

  let draftName = $state(profile.name);
  let draftUsername = $state(profile.username);
  let draftBio = $state(profile.bio);
  let draftCity = $state(profile.city);
  let draftWebsite = $state(profile.website);
  let draftInterests = $state(new Set(profile.interests));
  let fileInput: HTMLInputElement;

  const cities = TURKISH_CITIES;
  const interestOptions: { id: EventCategory; labelKey: string }[] = [
    { id: 'concert', labelKey: 'filters.category_concert' },
    { id: 'festival', labelKey: 'filters.category_festival' },
    { id: 'sport', labelKey: 'filters.category_sport' },
    { id: 'art', labelKey: 'filters.category_art' },
  ];

  function toggleInterest(id: EventCategory) {
    if (draftInterests.has(id)) draftInterests.delete(id);
    else draftInterests.add(id);
    draftInterests = new Set(draftInterests);
  }

  function onAvatarChange(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    setAvatar(URL.createObjectURL(file));
  }

  function save(e: Event) {
    e.preventDefault();
    setName(draftName.trim() || profile.name);
    setUsername(draftUsername.trim());
    setBio(draftBio.trim());
    setCity(draftCity);
    setWebsite(draftWebsite.trim());
    setInterests([...draftInterests]);
    goto('/profile');
  }
</script>

<div class="min-h-screen px-6 py-8 max-w-sm mx-auto space-y-8">
  <div class="flex items-center gap-3">
    <a
      href="/profile"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('profile.edit_profile')}</h1>
  </div>

  <form class="space-y-6" onsubmit={save}>
    <div class="flex justify-center">
      <div class="relative">
        <div
          class="w-24 h-24 rounded-full bg-[#dcfce7] dark:bg-[#1e3a2f] flex items-center justify-center shadow-xs overflow-hidden"
        >
          {#if profile.avatarUrl}
            <img
              src={profile.avatarUrl}
              alt={t('profile.change_avatar')}
              class="w-full h-full object-cover"
            />
          {:else}
            <span class="text-2xl text-emerald-600 dark:text-emerald-400 font-semibold select-none"
              >AH</span
            >
          {/if}
        </div>
        <button
          type="button"
          aria-label={t('profile.change_avatar')}
          onclick={() => fileInput.click()}
          class="absolute bottom-0 right-0 w-7 h-7 rounded-full bg-primary border-2 border-background flex items-center justify-center text-primary-foreground shadow-xs hover:bg-[#dc2626] transition-colors cursor-pointer"
        >
          <Camera class="w-3 h-3" />
        </button>
        <input
          bind:this={fileInput}
          onchange={onAvatarChange}
          type="file"
          accept="image/*"
          class="hidden"
        />
      </div>
    </div>

    <div class="space-y-1.5">
      <label for="name" class="text-xs font-medium text-foreground/80"
        >{t('register.full_name')}</label
      >
      <input
        id="name"
        type="text"
        bind:value={draftName}
        placeholder={t('register.full_name_placeholder')}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <label for="username" class="text-xs font-medium text-foreground/80"
        >{t('profile.username_label')}</label
      >
      <input
        id="username"
        type="text"
        bind:value={draftUsername}
        placeholder={t('profile.username_placeholder')}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <label for="bio" class="text-xs font-medium text-foreground/80"
        >{t('profile.bio_label')}</label
      >
      <textarea
        id="bio"
        rows="3"
        bind:value={draftBio}
        placeholder={t('profile.bio_placeholder')}
        class="w-full px-4 py-3 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all resize-none"
      ></textarea>
    </div>

    <div class="space-y-1.5">
      <label for="city" class="text-xs font-medium text-foreground/80"
        >{t('profile.city_label')}</label
      >
      <select
        id="city"
        bind:value={draftCity}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      >
        <option value="">{t('profile.city_placeholder')}</option>
        {#each cities as city}
          <option value={city}>{city}</option>
        {/each}
      </select>
    </div>

    <div class="space-y-1.5">
      <label for="website" class="text-xs font-medium text-foreground/80"
        >{t('profile.website_label')}</label
      >
      <input
        id="website"
        type="url"
        bind:value={draftWebsite}
        placeholder={t('profile.website_placeholder')}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <span class="text-xs font-medium text-foreground/80">{t('profile.interests_label')}</span>
      <div class="grid grid-cols-2 gap-2.5">
        {#each interestOptions as option (option.id)}
          {@const active = draftInterests.has(option.id)}
          <button
            type="button"
            onclick={() => toggleInterest(option.id)}
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

    <button
      type="submit"
      class="w-full h-12 rounded-2xl bg-primary text-primary-foreground font-semibold text-sm shadow-sm hover:bg-[#dc2626] active:scale-[0.99] transition-all cursor-pointer"
    >
      {t('common.save')}
    </button>
  </form>
</div>
