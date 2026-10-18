<!--
  @component SettingsPage
  @desc Application and account preferences screen (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-4 space-y-4 max-w-md mx-auto">
  <div class="flex items-center justify-between border-b border-border pb-3">
    <h1 class="text-xl font-bold">Ayarlar (Settings)</h1>
    <a
      href="/(tabs)/profile"
      class="text-xs text-primary min-h-[44px] min-w-[44px] inline-flex items-center justify-center"
    >
      {t('common.back')}
    </a>
  </div>

  <div class="space-y-2">
    <a
      href="/settings/following"
      class="flex items-center justify-between p-3 rounded-lg border border-border bg-card text-sm min-h-[44px] hover:bg-accent transition-colors"
    >
      <span>Takip Edilenler</span>
      <span class="text-muted-foreground text-xs">→</span>
    </a>

    <a
      href="/about"
      class="flex items-center justify-between p-3 rounded-lg border border-border bg-card text-sm min-h-[44px] hover:bg-accent transition-colors"
    >
      <span>Hakkında</span>
      <span class="text-muted-foreground text-xs">→</span>
    </a>
  </div>
</div>
