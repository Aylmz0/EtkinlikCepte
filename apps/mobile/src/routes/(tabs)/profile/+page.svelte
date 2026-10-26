<!--
  @component ProfilePage
  @desc User profile screen (§1.6, Owner: P6 Abdullah Hilal). The avatar badge
    lets the user preview a locally chosen photo (object URL, not uploaded —
    actual avatar storage is backend-dependent and not wired here). Name and
    avatar come from the shared profile store, also edited on /profile/edit.
  Props: None
  Events: None
-->
<script lang="ts">
  import {
    Camera,
    Settings,
    MessageSquare,
    ImagePlus,
    CalendarPlus,
    Building2,
    Heart,
    Users,
    ChevronRight,
  } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { profile, setAvatar } from '$lib/profile.svelte.js';

  let fileInput: HTMLInputElement;

  function onAvatarChange(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    setAvatar(URL.createObjectURL(file));
  }

  const stats = [
    { labelKey: 'profile.stat_events', value: '12' },
    { labelKey: 'profile.stat_clubs', value: '3' },
    { labelKey: 'profile.stat_points', value: '480' },
  ];
</script>

<div class="flex flex-col min-h-screen px-6 py-8 max-w-sm mx-auto space-y-6">
  <!-- Top bar: settings shortcut -->
  <div class="flex items-center justify-end">
    <a
      href="/settings"
      aria-label={t('home.settings')}
      class="w-10 h-10 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <Settings class="w-4 h-4" />
    </a>
  </div>

  <!-- Avatar + name -->
  <div class="flex flex-col items-center text-center space-y-3">
    <div class="relative">
      <div
        class="w-28 h-28 rounded-full bg-[#dcfce7] dark:bg-[#1e3a2f] flex items-center justify-center shadow-xs overflow-hidden"
      >
        {#if profile.avatarUrl}
          <img
            src={profile.avatarUrl}
            alt={t('profile.change_avatar')}
            class="w-full h-full object-cover"
          />
        {:else}
          <span class="text-3xl text-emerald-600 dark:text-emerald-400 font-semibold select-none"
            >AH</span
          >
        {/if}
      </div>
      <button
        type="button"
        aria-label={t('profile.change_avatar')}
        onclick={() => fileInput.click()}
        class="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-primary border-2 border-background flex items-center justify-center text-primary-foreground shadow-xs hover:bg-[#dc2626] transition-colors cursor-pointer"
      >
        <Camera class="w-3.5 h-3.5" />
      </button>
      <input
        bind:this={fileInput}
        onchange={onAvatarChange}
        type="file"
        accept="image/*"
        class="hidden"
      />
    </div>

    <div class="space-y-2">
      <h1 class="text-xl font-bold tracking-tight text-foreground leading-tight">
        {profile.name}
      </h1>
      {#if profile.username}
        <p class="text-xs text-[#ea580c] font-medium">@{profile.username}</p>
      {/if}
      {#if profile.bio}
        <p class="text-xs text-muted-foreground max-w-[220px]">{profile.bio}</p>
      {/if}
      <a
        href="/profile/edit"
        class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-xl bg-primary text-primary-foreground text-xs font-medium shadow-xs hover:bg-[#dc2626] transition-colors"
      >
        {t('profile.edit_profile')}
      </a>
    </div>
  </div>

  <!-- Stats row -->
  <div class="grid grid-cols-3 gap-2.5">
    {#each stats as stat}
      <div
        class="rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs py-3 text-center"
      >
        <span class="block text-lg font-black text-foreground">{stat.value}</span>
        <span class="block text-[11px] text-muted-foreground">{t(stat.labelKey)}</span>
      </div>
    {/each}
  </div>

  <!-- Quick access tiles -->
  <div class="space-y-2.5">
    <a
      href="/profile/create-event"
      class="flex items-center justify-between p-4 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-primary/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <div
          class="w-9 h-9 rounded-xl bg-[#fef2e8] dark:bg-[#2a221b] text-[#ea580c] flex items-center justify-center"
        >
          <CalendarPlus class="w-4 h-4" />
        </div>
        <span class="text-sm font-bold text-foreground">{t('createEvent.tile')}</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <a
      href="/profile/create-club"
      class="flex items-center justify-between p-4 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-primary/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <div
          class="w-9 h-9 rounded-xl bg-[#fef2e8] dark:bg-[#2a221b] text-[#ea580c] flex items-center justify-center"
        >
          <Building2 class="w-4 h-4" />
        </div>
        <span class="text-sm font-bold text-foreground">{t('createClub.tile')}</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <a
      href="/settings/following"
      class="flex items-center justify-between p-4 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-primary/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <div
          class="w-9 h-9 rounded-xl bg-[#fef2e8] dark:bg-[#2a221b] text-[#ea580c] flex items-center justify-center"
        >
          <Heart class="w-4 h-4" />
        </div>
        <span class="text-sm font-bold text-foreground">{t('settingsFollowing.title')}</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <a
      href="/profile/clubs"
      class="flex items-center justify-between p-4 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-primary/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <div
          class="w-9 h-9 rounded-xl bg-[#fef2e8] dark:bg-[#2a221b] text-[#ea580c] flex items-center justify-center"
        >
          <Users class="w-4 h-4" />
        </div>
        <span class="text-sm font-bold text-foreground">{t('profile.my_clubs')}</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <a
      href="/profile/posts"
      class="flex items-center justify-between p-4 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-primary/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <div
          class="w-9 h-9 rounded-xl bg-[#fef2e8] dark:bg-[#2a221b] text-[#ea580c] flex items-center justify-center"
        >
          <ImagePlus class="w-4 h-4" />
        </div>
        <span class="text-sm font-bold text-foreground">{t('profile.my_posts')}</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <a
      href="/messages"
      class="flex items-center justify-between p-4 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-primary/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <div
          class="w-9 h-9 rounded-xl bg-[#e6faf8] dark:bg-[#102a28] text-[#00c4b4] flex items-center justify-center"
        >
          <MessageSquare class="w-4 h-4" />
        </div>
        <span class="text-sm font-bold text-foreground">{t('profile.chats')}</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>
  </div>
</div>
