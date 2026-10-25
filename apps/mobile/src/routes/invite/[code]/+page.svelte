<!--
  @component InviteAcceptPage
  @desc Club and event invite confirmation screen (§1.6, Owner: P2). Accepting
    or declining joins/leaves a club on the backend and is not wired here —
    the buttons are visually ready but inert.
  Props: None
  Events: None
-->
<script lang="ts">
  import { page } from '$app/state';
  import { Users, MapPin } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
</script>

<div class="min-h-screen px-6 py-10 max-w-sm mx-auto flex flex-col justify-center">
  <div
    class="rounded-3xl bg-white dark:bg-card border border-border/80 p-6 shadow-sm space-y-5 text-center"
  >
    <div
      class="w-16 h-16 mx-auto rounded-full bg-[#fef2e8] dark:bg-[#2a221b] flex items-center justify-center text-[#ea580c]"
    >
      <Users class="w-7 h-7" />
    </div>

    <div class="space-y-1.5">
      <h1 class="text-xl font-bold tracking-tight text-foreground">{t('invite.heading')}</h1>
      <div class="flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
        <MapPin class="w-3.5 h-3.5" />
        <span>{t('invite.code_label')}: {page.params.code}</span>
      </div>
    </div>

    <p class="text-xs text-muted-foreground leading-relaxed">
      {t('invite.body')}
    </p>

    <div class="flex gap-3 pt-1">
      <button
        type="button"
        class="flex-1 h-12 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground font-semibold text-sm shadow-xs hover:bg-muted/40 transition-colors cursor-pointer"
      >
        {t('invite.decline')}
      </button>
      <button
        type="button"
        class="flex-1 h-12 rounded-2xl bg-primary text-primary-foreground font-semibold text-sm shadow-sm hover:bg-[#dc2626] transition-colors cursor-pointer"
      >
        {t('invite.accept')}
      </button>
    </div>
  </div>
</div>
