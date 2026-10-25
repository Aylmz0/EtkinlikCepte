<!--
  @component ForgotPasswordPage
  @desc Password reset request screen, reached from Login's "Şifrenizi mi
    unuttunuz?" link (§1.6). Actually sending a reset email is
    backend-dependent and not wired here — submitting just shows a
    frontend-only confirmation state.
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, MailCheck } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  let email = $state('');
  let submitted = $state(false);

  function submit(e: Event) {
    e.preventDefault();
    if (!email.trim()) return;
    submitted = true;
  }
</script>

<div class="flex flex-col min-h-screen px-6 py-10 max-w-sm mx-auto">
  <a
    href="/login"
    aria-label={t('common.back')}
    class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
  >
    <ArrowLeft class="w-4 h-4" />
  </a>

  {#if submitted}
    <div class="flex-1 flex flex-col items-center justify-center text-center gap-3 pb-10">
      <div
        class="w-16 h-16 rounded-full bg-[#fef2e8] dark:bg-[#2a221b] flex items-center justify-center text-[#ea580c]"
      >
        <MailCheck class="w-7 h-7" />
      </div>
      <h1 class="text-xl font-bold tracking-tight text-foreground">
        {t('forgotPassword.success_heading')}
      </h1>
      <p class="text-xs text-muted-foreground max-w-[260px]">
        {t('forgotPassword.success_body')}
        <span class="font-semibold text-foreground">{email}</span>
      </p>
      <a
        href="/login"
        class="mt-2 inline-flex items-center justify-center px-5 h-11 rounded-2xl bg-primary text-primary-foreground font-semibold text-sm shadow-sm hover:bg-[#dc2626] transition-colors"
      >
        {t('forgotPassword.back_to_login')}
      </a>
    </div>
  {:else}
    <div class="pt-8 space-y-8">
      <div class="space-y-2">
        <h1 class="text-2xl font-bold tracking-tight text-foreground leading-snug">
          {t('forgotPassword.title')}
        </h1>
        <p class="text-xs text-muted-foreground leading-relaxed">
          {t('forgotPassword.heading')}
        </p>
      </div>

      <form class="space-y-5" onsubmit={submit}>
        <div class="space-y-1.5">
          <label for="reset-email" class="text-xs font-medium text-foreground/80"
            >{t('auth.email')}</label
          >
          <!-- svelte-ignore a11y_autofocus -- single-field form, same as other auth screens -->
          <input
            id="reset-email"
            type="email"
            bind:value={email}
            placeholder={t('login.email_placeholder')}
            autofocus
            class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
          />
        </div>

        <button
          type="submit"
          disabled={!email.trim()}
          class="w-full h-13 rounded-2xl font-semibold text-base shadow-sm transition-all {email.trim()
            ? 'bg-primary text-primary-foreground hover:bg-[#dc2626] active:scale-[0.99] cursor-pointer'
            : 'bg-primary/40 text-primary-foreground cursor-not-allowed'}"
        >
          {t('forgotPassword.submit')}
        </button>
      </form>
    </div>
  {/if}
</div>
