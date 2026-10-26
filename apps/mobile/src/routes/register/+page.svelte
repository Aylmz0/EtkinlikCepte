<!--
  @component RegisterPage
  @desc Authentication register screen matching UI mockup Image 4 (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { session } from '$lib/auth/session.svelte';
  import { t } from '$lib/i18n.js';

  let fullName = $state('');
  let email = $state('');
  let password = $state('');
  let passwordConfirm = $state('');
  let error = $state('');
  let busy = $state(false);

  async function submit(event: SubmitEvent) {
    event.preventDefault();
    if (password !== passwordConfirm) {
      error = t('register.password_mismatch');
      return;
    }
    busy = true;
    error = '';
    try {
      await session.register(email, password, fullName);
      await goto('/discover');
    } catch {
      error = t('register.failed');
    } finally {
      busy = false;
    }
  }
</script>

<div class="flex flex-col min-h-screen px-6 py-10 max-w-sm mx-auto justify-between">
  <!-- Top section / form -->
  <div class="pt-6 space-y-6">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">{t('register.heading')}</h1>

    <form class="space-y-4" onsubmit={submit}>
      <div class="space-y-1.5">
        <label for="fullName" class="text-xs font-medium text-foreground/80"
          >{t('register.full_name')}</label
        >
        <input
          id="fullName"
          type="text"
          placeholder={t('register.full_name_placeholder')}
          bind:value={fullName}
          autocomplete="name"
          required
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>

      <div class="space-y-1.5">
        <label for="email" class="text-xs font-medium text-foreground/80">{t('auth.email')}</label>
        <input
          id="email"
          type="email"
          placeholder={t('register.email_placeholder')}
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
          placeholder={t('register.password_placeholder')}
          bind:value={password}
          autocomplete="new-password"
          required
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>

      <div class="space-y-1.5">
        <label for="passwordConfirm" class="text-xs font-medium text-foreground/80"
          >{t('register.password_confirm')}</label
        >
        <input
          id="passwordConfirm"
          type="password"
          placeholder={t('register.password_confirm_placeholder')}
          bind:value={passwordConfirm}
          autocomplete="new-password"
          required
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>

      <div class="pt-4">
        <button
          type="submit"
          class="w-full h-13 rounded-2xl bg-primary text-primary-foreground font-semibold text-base shadow-sm hover:bg-[#dc2626] active:scale-[0.99] transition-all cursor-pointer"
          disabled={busy}
        >
          {busy ? t('common.loading') : t('auth.register')}
        </button>
      </div>
      {#if error}<p class="text-xs text-destructive">{error}</p>{/if}
    </form>
  </div>

  <footer class="py-6 text-center text-xs text-muted-foreground">
    <span>{t('register.has_account')}</span>
    <a href="/login" class="font-semibold text-primary hover:underline ml-1">
      {t('auth.login')}
    </a>
  </footer>
</div>
