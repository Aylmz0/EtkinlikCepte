<!--
  @component EventDetailPage
  @desc Event details, location, schedule, and ticket action (§1.6, Owner: P7).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-4 space-y-4 max-w-md mx-auto">
  <div class="flex items-center justify-between border-b border-border pb-3">
    <h1 class="text-xl font-bold">Etkinlik Detay</h1>
    <a
      href="/(tabs)/discover"
      class="text-xs text-primary min-h-[44px] min-w-[44px] inline-flex items-center justify-center"
    >
      {t('common.back')}
    </a>
  </div>
  <p class="text-sm text-muted-foreground">P7 Ownership</p>

  <div class="pt-4 flex gap-3">
    <a
      href="/events/1/tickets"
      class="flex-1 min-h-[44px] inline-flex items-center justify-center rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
    >
      Bilet Seç
    </a>
    <a
      href="/events/1/room"
      class="flex-1 min-h-[44px] inline-flex items-center justify-center rounded-lg border border-border bg-card text-foreground text-sm font-medium hover:bg-accent transition-colors"
    >
      Oda (Online)
    </a>
  </div>
</div>
