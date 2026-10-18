<!--
  @component DiscoverPage
  @desc Map and event list discovery screen (§1.6, Owner: P7).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-4 space-y-4">
  <div class="flex items-center justify-between">
    <h1 class="text-xl font-bold">{t('nav.discover')}</h1>
    <span class="text-xs px-2 py-0.5 rounded bg-muted text-muted-foreground">P7</span>
  </div>
  <p class="text-sm text-muted-foreground">
    {t('app.name')} • {t('nav.discover')}
  </p>
</div>
