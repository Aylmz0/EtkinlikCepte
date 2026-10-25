<!--
  @component MyClubsPage
  @desc "Kulüplerim" — the clubs the user follows, each with its info plus
    direct shortcuts into its member list and group chat (§1.6).
  Props: None
  Events: None
-->
<script lang="ts">
  import { MapPin, Users, MessageSquare, ChevronRight } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { clubs, followedClubIds } from '$lib/clubs.svelte.js';

  let myClubs = $derived(clubs.filter((c) => followedClubIds.has(c.id)));
</script>

<div class="px-5 py-4 space-y-5 max-w-sm mx-auto">
  <!-- Title -->
  <div class="space-y-1 pt-1">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">{t('profile.my_clubs')}</h1>
    <p class="text-xs text-muted-foreground">{t('profile.my_clubs_subtitle')}</p>
  </div>

  {#if myClubs.length === 0}
    <p class="text-sm text-muted-foreground text-center py-10">{t('profile.my_clubs_empty')}</p>
  {/if}

  <div class="space-y-3">
    {#each myClubs as club (club.id)}
      <div
        class="rounded-3xl bg-white dark:bg-card border border-border/80 shadow-xs overflow-hidden"
      >
        <a
          href="/clubs/{club.id}"
          class="flex items-center gap-3 p-3.5 hover:bg-muted/30 transition-colors"
        >
          <img
            src={club.image}
            alt={club.title}
            class="w-14 h-14 rounded-2xl object-cover shrink-0"
          />
          <div class="flex-1 min-w-0 space-y-0.5">
            <h2 class="text-sm font-bold text-foreground leading-snug line-clamp-1">
              {club.title}
            </h2>
            <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
              <MapPin class="w-3 h-3 text-[#ea580c]" />
              <span class="line-clamp-1">{club.address}</span>
            </div>
            <p class="text-[11px] text-muted-foreground/80 line-clamp-1">{t(club.categoryKey)}</p>
          </div>
          <ChevronRight class="w-4 h-4 text-muted-foreground/60 shrink-0" />
        </a>

        <div class="grid grid-cols-2 border-t border-border/60">
          <a
            href="/clubs/{club.id}/followers"
            class="flex items-center justify-center gap-1.5 py-2.5 text-xs font-semibold text-foreground hover:bg-muted/30 transition-colors border-r border-border/60"
          >
            <Users class="w-3.5 h-3.5 text-[#ea580c]" />
            {t('clubDetail.followers')}
          </a>
          <a
            href="/clubs/{club.id}/chat"
            class="flex items-center justify-center gap-1.5 py-2.5 text-xs font-semibold text-foreground hover:bg-muted/30 transition-colors"
          >
            <MessageSquare class="w-3.5 h-3.5 text-[#ea580c]" />
            {t('clubDetail.chat')}
          </a>
        </div>
      </div>
    {/each}
  </div>
</div>
