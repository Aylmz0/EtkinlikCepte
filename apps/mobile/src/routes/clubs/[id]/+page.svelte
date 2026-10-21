<!--
  @component ClubDetailPage
  @desc Club profile, description, member list, and actions (§1.6, Owners: P2, P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="p-4 space-y-4 max-w-md mx-auto">
  <div class="flex items-center justify-between border-b border-border pb-3">
    <h1 class="text-xl font-bold">Kulüp Detay</h1>
    <a
      href="/(tabs)/clubs"
      class="text-xs text-primary min-h-[44px] min-w-[44px] inline-flex items-center justify-center"
    >
      {t('common.back')}
    </a>
  </div>
  <p class="text-sm text-muted-foreground">P2, P6 (Abdullah Hilal)</p>

  <div class="pt-4 grid grid-cols-2 gap-2">
    <a
      href="/clubs/1/chat"
      class="p-3 rounded-lg border border-border bg-card text-center text-xs font-medium hover:bg-accent transition-colors"
    >
      Kulüp Sohbeti (P5)
    </a>
    <a
      href="/clubs/1/followers"
      class="p-3 rounded-lg border border-border bg-card text-center text-xs font-medium hover:bg-accent transition-colors"
    >
      Takipçiler (P2)
    </a>
    <a
      href="/clubs/1/new-post"
      class="p-3 rounded-lg border border-border bg-card text-center text-xs font-medium hover:bg-accent transition-colors"
    >
      Gönderi Paylaş (P2)
    </a>
  </div>
</div>
