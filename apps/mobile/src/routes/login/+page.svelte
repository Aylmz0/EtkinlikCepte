<!--
  @component LoginPage
  @desc Authentication login screen matching UI mockup Image 3 (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { session } from '$lib/auth/session.svelte';
  import { t } from '$lib/i18n.js';

  let email = $state('');
  let password = $state('');
  let error = $state('');
  let busy = $state(false);

  async function submit(event: SubmitEvent) {
    event.preventDefault();
    busy = true;
    error = '';
    try {
      await session.login(email, password);
      await goto('/discover');
    } catch {
      error = t('login.failed');
    } finally {
      busy = false;
    }
  }
</script>

<div class="flex flex-col min-h-screen px-6 py-10 max-w-sm mx-auto justify-between">
  <!-- Top spacing / brand -->
  <div class="pt-8 space-y-8">
    <h1 class="text-2xl font-bold tracking-tight text-foreground leading-snug">
      {t('login.heading')}
    </h1>

    <form class="space-y-5" onsubmit={submit}>
      <div class="space-y-1.5">
        <label for="email" class="text-xs font-medium text-foreground/80">{t('auth.email')}</label>
        <input
          id="email"
          type="email"
          placeholder={t('login.email_placeholder')}
          bind:value={email}
          autocomplete="email"
          required
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>

      <div class="space-y-1.5">
        <label for="password" class="text-xs font-medium text-foreground/80"
          >{t('auth.password')}</label
        >
        <input
          id="password"
          type="password"
          placeholder={t('login.password_placeholder')}
          bind:value={password}
          autocomplete="current-password"
          required
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
        <div class="flex justify-end pt-1">
          <a href="/forgot-password" class="text-xs font-medium text-primary hover:underline">
            {t('login.forgot_password')}
          </a>
        </div>
      </div>

      <div class="pt-4">
        <button
          type="submit"
          class="w-full h-13 rounded-2xl bg-primary text-primary-foreground font-semibold text-base shadow-sm hover:bg-[#dc2626] active:scale-[0.99] transition-all cursor-pointer"
          disabled={busy}
        >
          {busy ? t('common.loading') : t('auth.login')}
        </button>
      </div>
      {#if error}<p class="text-xs text-destructive">{error}</p>{/if}
    </form>
  </div>

  <footer class="py-6 text-center text-xs text-muted-foreground">
    <span>{t('login.no_account')}</span>
    <a href="/register" class="font-semibold text-primary hover:underline ml-1">
      {t('auth.register')}
    </a>
  </footer>
</div>
