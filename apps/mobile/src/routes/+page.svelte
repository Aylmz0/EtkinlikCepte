<!--
  @component HomePage
  @desc Root landing and quick launch hub for the mobile shell.
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<main class="flex flex-col min-h-screen px-6 py-8 max-w-sm mx-auto justify-between">
  <!-- Brand Header -->
  <header class="pt-6 space-y-3">
    <h1 class="text-4xl font-black tracking-tight text-foreground">
      Keşfet<span class="text-primary">.</span>
    </h1>
    <p class="text-sm text-muted-foreground leading-relaxed">
      {t('app.tagline')}
    </p>
  </header>

  <!-- Auth entry points -->
  <section class="space-y-3 my-auto py-6">
    <a
      href="/login"
      class="h-12 rounded-2xl bg-primary text-primary-foreground font-semibold text-sm flex items-center justify-center shadow-xs hover:bg-[#dc2626] transition-colors"
    >
      {t('auth.login')}
    </a>
    <a
      href="/register"
      class="h-12 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground font-semibold text-sm flex items-center justify-center shadow-xs hover:bg-muted/40 transition-colors"
    >
      {t('auth.register')}
    </a>
    <a
      href="/discover"
      class="h-12 rounded-2xl text-muted-foreground font-medium text-sm flex items-center justify-center hover:text-foreground transition-colors"
    >
      {t('home.continue_without_login')}
    </a>
  </section>
</main>
