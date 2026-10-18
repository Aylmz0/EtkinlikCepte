<!--
  @component ClubsPage
  @desc Clubs discovery and joined clubs list (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-4 space-y-4">
  <div class="flex items-center justify-between">
    <h1 class="text-xl font-bold">{t('nav.clubs')}</h1>
    <span class="text-xs px-2 py-0.5 rounded bg-primary/10 text-primary font-medium"
      >P6 (Abdullah Hilal)</span
    >
  </div>
  <p class="text-sm text-muted-foreground">
    {t('app.name')} • {t('nav.clubs')}
  </p>
</div>
