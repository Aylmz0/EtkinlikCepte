<!--
  @component SettingsFollowingPage
  @desc Clubs/venues the user follows — the same follow state toggled on a
    club's own detail page (§1.6). Reachable from both Profile and Settings.
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, UserMinus } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { clubs, followedClubIds, toggleFollow } from '$lib/clubs.svelte.js';

  let followedClubs = $derived(clubs.filter((c) => followedClubIds.has(c.id)));
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto space-y-5 pb-12">
  <div class="flex items-center gap-3 pt-2">
    <a
      href="/settings"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">
      {t('settingsFollowing.title')}
    </h1>
  </div>

  {#if followedClubs.length === 0}
    <p class="text-sm text-muted-foreground text-center py-10">{t('settingsFollowing.empty')}</p>
  {/if}

  <div class="space-y-3">
    {#each followedClubs as club (club.id)}
      <div
        class="flex items-center gap-3 p-3 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs"
      >
        <a href="/clubs/{club.id}" class="flex items-center gap-3 flex-1 min-w-0">
          <img
            src={club.image}
            alt={club.title}
            class="w-12 h-12 rounded-xl object-cover shrink-0"
          />
          <div class="min-w-0 space-y-0.5">
            <h3 class="text-sm font-semibold text-foreground leading-snug line-clamp-1">
              {club.title}
            </h3>
            <p class="text-xs text-muted-foreground leading-snug line-clamp-1">{club.address}</p>
          </div>
        </a>
        <button
          type="button"
          aria-label={t('settingsFollowing.unfollow')}
          onclick={() => toggleFollow(club.id)}
          class="w-9 h-9 rounded-xl bg-muted text-muted-foreground hover:bg-destructive/10 hover:text-destructive flex items-center justify-center transition-colors cursor-pointer shrink-0"
        >
          <UserMinus class="w-4 h-4" />
        </button>
      </div>
    {/each}
  </div>
</div>
