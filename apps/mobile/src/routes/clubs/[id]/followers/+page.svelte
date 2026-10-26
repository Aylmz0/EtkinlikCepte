<!--
  @component ClubFollowersPage
  @desc Club follower and member roster (§1.6, Owner: P2).
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  const followers = [
    { id: '1', name: 'Kullanıcı adı', since: '26.03.2026' },
    { id: '2', name: 'Kullanıcı adı', since: '23.06.2026' },
    { id: '3', name: 'Kullanıcı adı', since: '09.11.2026' },
  ];
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto space-y-5 pb-12">
  <div class="flex items-center gap-3 pt-2">
    <a
      href="../"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('clubFollowers.title')}</h1>
  </div>

  <div class="space-y-3.5">
    {#each followers as follower (follower.id)}
      <div class="flex items-center gap-3">
        <div
          class="w-12 h-12 rounded-full bg-[#dcfce7] dark:bg-[#1e3a2f] flex items-center justify-center shrink-0 shadow-xs"
        >
          <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400 select-none">
            {follower.name.slice(0, 2).toUpperCase()}
          </span>
        </div>
        <div
          class="flex-1 h-12 px-4 rounded-2xl bg-white dark:bg-card border border-border/80 flex items-center justify-between shadow-xs"
        >
          <span class="text-xs font-semibold text-foreground">{follower.name}</span>
          <span class="text-[11px] text-muted-foreground"
            >{t('clubDetail.following_since')}: {follower.since}</span
          >
        </div>
      </div>
    {/each}
  </div>
</div>
