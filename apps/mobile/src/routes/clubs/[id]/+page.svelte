<!--
  @component ClubDetailPage
  @desc Club profile, description, and actions (§1.6, Owners: P2, P6). Looks
    the club up from the shared mock catalogue by route id (§1.4).
  Props: None
  Events: None
-->
<script lang="ts">
  import { page } from '$app/state';
  import {
    ArrowLeft,
    MapPin,
    MessageSquare,
    Users,
    ImagePlus,
    UserPlus,
    UserMinus,
  } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { clubs, isFollowed, toggleFollow } from '$lib/clubs.svelte.js';

  let club = $derived(clubs.find((c) => c.id === page.params.id) ?? clubs[0]);
  let following = $derived(isFollowed(club.id));

  const actions = [
    { href: './chat', labelKey: 'clubDetail.chat', icon: MessageSquare },
    { href: './followers', labelKey: 'clubDetail.followers', icon: Users },
    { href: './new-post', labelKey: 'clubDetail.new_post', icon: ImagePlus },
  ];
</script>

<div class="app-canvas min-h-screen pb-12">
  <!-- Hero, follow button, info card, and action grid all share this single
       max-w-sm column so every component ends up the same width. -->
  <main class="px-5 pt-6 max-w-sm mx-auto space-y-4">
    <div class="relative w-full aspect-[4/2.6] rounded-[2.5rem] overflow-hidden shadow-md">
      <img src={club.image} alt={club.title} class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/20 to-black/20"></div>

      <div class="absolute top-5 left-5 right-5 flex items-center justify-between z-10">
        <a
          href="/clubs"
          aria-label={t('common.back')}
          class="w-10 h-10 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center shadow-sm hover:bg-white transition-colors"
        >
          <ArrowLeft class="w-4 h-4 text-[#ef4444]" />
        </a>
      </div>

      <div class="absolute bottom-5 left-5 right-5 text-white">
        <h1 class="text-2xl font-black tracking-tight drop-shadow-sm">{club.title}</h1>
        <div class="flex items-center gap-1.5 text-xs text-white/90 pt-1">
          <MapPin class="w-3.5 h-3.5 text-white/80" />
          <span>{club.address}</span>
        </div>
      </div>
    </div>

    <button
      type="button"
      onclick={() => toggleFollow(club.id)}
      class="w-full h-12 rounded-2xl font-semibold text-sm flex items-center justify-center gap-2 shadow-xs transition-colors cursor-pointer {following
        ? 'bg-white dark:bg-card border border-border/80 text-foreground hover:bg-muted/40'
        : 'bg-primary text-primary-foreground hover:bg-[#dc2626]'}"
    >
      {#if following}
        <UserMinus class="w-4 h-4" />
        <span>{t('clubDetail.unfollow')}</span>
      {:else}
        <UserPlus class="w-4 h-4" />
        <span>{t('clubDetail.follow')}</span>
      {/if}
    </button>

    <div class="rounded-3xl bg-white dark:bg-card border border-border/80 p-5 shadow-xs space-y-3">
      <h2 class="text-lg font-bold text-foreground">{t('clubDetail.about')}</h2>
      <p class="text-xs text-muted-foreground leading-relaxed">
        {club.description}
      </p>
    </div>

    <div class="grid grid-cols-3 gap-2.5">
      {#each actions as action}
        {@const Icon = action.icon}
        <a
          href={action.href}
          class="flex flex-col items-center justify-center p-3.5 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-[#ea580c]/30 hover:shadow-sm transition-all text-center gap-1.5"
        >
          <Icon class="w-4.5 h-4.5 text-[#ea580c]" />
          <span class="text-[11px] font-semibold text-foreground leading-tight"
            >{t(action.labelKey)}</span
          >
        </a>
      {/each}
    </div>
  </main>
</div>
