<!--
  @component HomePage
  @desc Root landing page and navigation hub for the mobile shell.
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<main class="flex flex-col min-h-screen p-6 max-w-md mx-auto justify-between">
  <header class="pt-8 pb-4 space-y-2">
    <div
      class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20"
    >
      <span>{t('app.name')}</span>
      <span>•</span>
      <span>v0.1.0</span>
    </div>
    <h1 class="text-3xl font-bold tracking-tight text-foreground">
      {t('app.name')}
    </h1>
    <p class="text-sm text-muted-foreground">
      {t('app.tagline')}
    </p>
  </header>

  <section class="space-y-4 my-auto">
    <div class="grid grid-cols-2 gap-3">
      <a
        href="/(tabs)/discover"
        class="flex flex-col p-4 rounded-xl border border-border bg-card text-card-foreground shadow-sm hover:border-primary/50 transition-colors"
      >
        <span class="text-sm font-semibold">{t('nav.discover')}</span>
        <span class="text-xs text-muted-foreground mt-1">/(tabs)/discover</span>
      </a>

      <a
        href="/(tabs)/clubs"
        class="flex flex-col p-4 rounded-xl border border-border bg-card text-card-foreground shadow-sm hover:border-primary/50 transition-colors"
      >
        <span class="text-sm font-semibold">{t('nav.clubs')}</span>
        <span class="text-xs text-muted-foreground mt-1">/(tabs)/clubs</span>
      </a>

      <a
        href="/(tabs)/tickets"
        class="flex flex-col p-4 rounded-xl border border-border bg-card text-card-foreground shadow-sm hover:border-primary/50 transition-colors"
      >
        <span class="text-sm font-semibold">{t('nav.tickets')}</span>
        <span class="text-xs text-muted-foreground mt-1">/(tabs)/tickets</span>
      </a>

      <a
        href="/(tabs)/profile"
        class="flex flex-col p-4 rounded-xl border border-border bg-card text-card-foreground shadow-sm hover:border-primary/50 transition-colors"
      >
        <span class="text-sm font-semibold">{t('nav.profile')}</span>
        <span class="text-xs text-muted-foreground mt-1">/(tabs)/profile</span>
      </a>
    </div>

    <div class="pt-2 flex gap-3">
      <a
        href="/login"
        class="flex-1 py-3 px-4 rounded-lg bg-primary text-primary-foreground font-medium text-sm text-center shadow-sm hover:bg-primary/90 transition-colors"
      >
        {t('auth.login')}
      </a>
      <a
        href="/register"
        class="flex-1 py-3 px-4 rounded-lg border border-border bg-card text-foreground font-medium text-sm text-center shadow-sm hover:bg-accent transition-colors"
      >
        {t('auth.register')}
      </a>
    </div>
  </section>

  <footer class="py-4 text-center text-xs text-muted-foreground">
    <span>EtkinlikCepte • H1.12 Skeleton</span>
  </footer>
</main>
