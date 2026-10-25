<!--
  @component ChangePasswordPage
  @desc Change account password (§1.6, Owner: P6). The actual password update
    call is backend-dependent and not wired here — inputs accept local text,
    submit stays inert.
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  let current = $state('');
  let next = $state('');
  let confirm = $state('');
</script>

<div class="min-h-screen px-6 py-10 max-w-sm mx-auto space-y-8">
  <div class="flex items-center gap-3">
    <a
      href="/settings"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('changePassword.title')}</h1>
  </div>

  <form class="space-y-5" onsubmit={(e) => e.preventDefault()}>
    <div class="space-y-1.5">
      <label for="current" class="text-xs font-medium text-foreground/80"
        >{t('changePassword.current')}</label
      >
      <input
        id="current"
        type="password"
        bind:value={current}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <label for="next" class="text-xs font-medium text-foreground/80"
        >{t('changePassword.new')}</label
      >
      <input
        id="next"
        type="password"
        bind:value={next}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <div class="space-y-1.5">
      <label for="confirm" class="text-xs font-medium text-foreground/80"
        >{t('changePassword.confirm')}</label
      >
      <input
        id="confirm"
        type="password"
        bind:value={confirm}
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <button
      type="submit"
      disabled
      class="w-full h-12 rounded-2xl bg-primary/40 text-primary-foreground font-semibold text-sm shadow-xs cursor-not-allowed"
    >
      {t('changePassword.submit')}
    </button>
  </form>
</div>
