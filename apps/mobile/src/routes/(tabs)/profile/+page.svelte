<!--
  @component ProfilePage
  @desc User profile, interests, city, language, and following settings (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-4 space-y-4">
  <div class="flex items-center justify-between">
    <h1 class="text-xl font-bold">{t('nav.profile')}</h1>
    <span class="text-xs px-2 py-0.5 rounded bg-primary/10 text-primary font-medium"
      >P6 (Abdullah Hilal)</span
    >
  </div>
  <p class="text-sm text-muted-foreground">
    {t('app.name')} • {t('nav.profile')}
  </p>

  <div class="pt-4">
    <a
      href="/settings"
      class="inline-flex items-center min-h-[44px] px-4 py-2 rounded-lg border border-border bg-card text-sm font-medium hover:bg-accent transition-colors"
    >
      Ayarlar (Settings)
    </a>
  </div>
</div>
