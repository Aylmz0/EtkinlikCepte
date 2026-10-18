<!--
  @component LoginPage
  @desc Authentication login screen (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-6 max-w-sm mx-auto space-y-6 pt-12">
  <div class="space-y-1 text-center">
    <h1 class="text-2xl font-bold">{t('auth.login')}</h1>
    <p class="text-xs text-muted-foreground">{t('app.name')}</p>
  </div>

  <div class="space-y-4">
    <div class="space-y-1">
      <label for="email" class="text-xs font-medium text-foreground">{t('auth.email')}</label>
      <input
        id="email"
        type="email"
        placeholder="ad@ornek.com"
        class="w-full h-11 px-3 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
      />
    </div>

    <div class="space-y-1">
      <label for="password" class="text-xs font-medium text-foreground">{t('auth.password')}</label>
      <input
        id="password"
        type="password"
        placeholder="••••••••"
        class="w-full h-11 px-3 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
      />
    </div>

    <button
      type="button"
      class="w-full h-11 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
    >
      {t('auth.submit')}
    </button>
  </div>

  <div class="text-center text-xs text-muted-foreground">
    <a href="/register" class="hover:underline">{t('auth.register')}</a>
  </div>
</div>
