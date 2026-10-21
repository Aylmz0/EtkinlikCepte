<!--
  @component ScannerPage
  @desc QR code door validation scanner (§1.6, Owners: P2, P7).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-4 space-y-4 max-w-md mx-auto">
  <div class="flex items-center justify-between border-b border-border pb-3">
    <h1 class="text-xl font-bold">Kapıda Doğrulama (Scanner)</h1>
    <a
      href="/"
      class="text-xs text-primary min-h-[44px] min-w-[44px] inline-flex items-center justify-center"
    >
      {t('common.back')}
    </a>
  </div>
  <p class="text-sm text-muted-foreground">P2, P7 Ownership</p>
</div>
