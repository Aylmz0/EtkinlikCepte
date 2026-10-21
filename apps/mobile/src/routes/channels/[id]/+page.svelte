<!--
  @component ChannelChatPage
  @desc Direct message 1-on-1 private channel (§1.6, Owner: P5).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-4 space-y-4 max-w-md mx-auto">
  <div class="flex items-center justify-between border-b border-border pb-3">
    <h1 class="text-xl font-bold">Özel Mesajlaşma</h1>
    <a
      href="/(tabs)/messages"
      class="text-xs text-primary min-h-[44px] min-w-[44px] inline-flex items-center justify-center"
    >
      {t('common.back')}
    </a>
  </div>
  <p class="text-sm text-muted-foreground">P5 Channel</p>

  <div class="pt-4">
    <a
      href="/channels/1/room"
      class="inline-flex items-center justify-center min-h-[44px] px-4 py-2 rounded-lg border border-border bg-card text-xs font-medium hover:bg-accent transition-colors"
    >
      Özel Görüşme Odası
    </a>
  </div>
</div>
