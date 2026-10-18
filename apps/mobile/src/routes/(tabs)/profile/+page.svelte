<!--
  @component ProfilePage
  @desc User profile screen matching UI mockup Image 1 (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
  import { Settings } from '@lucide/svelte';
</script>

<div class="flex flex-col min-h-screen px-6 py-8 max-w-sm mx-auto justify-between">
  <!-- Top Profile Card Section -->
  <div class="space-y-6 pt-4">
    <div class="flex items-center gap-6">
      <!-- Circular Avatar with subtle settings badge -->
      <div class="relative">
        <div
          class="w-28 h-28 rounded-full bg-[#dcfce7] dark:bg-[#1e3a2f] flex items-center justify-center shadow-xs"
        >
          <span class="text-3xl text-emerald-600 dark:text-emerald-400 font-semibold select-none"
            >AH</span
          >
        </div>
        <a
          href="/settings"
          aria-label="Ayarlar"
          class="absolute bottom-1 left-0 w-6 h-6 rounded-full bg-white dark:bg-card border border-border flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
        >
          <Settings class="w-3.5 h-3.5" />
        </a>
      </div>

      <!-- Username & Edit Badge -->
      <div class="space-y-3">
        <h1 class="text-2xl font-bold tracking-tight text-foreground leading-tight">
          Kullanıcı<br />Adı
        </h1>
        <div>
          <button
            type="button"
            class="inline-flex items-center justify-center px-3.5 py-1.5 rounded-xl bg-primary text-primary-foreground text-xs font-medium shadow-xs hover:bg-[#dc2626] transition-colors cursor-pointer"
          >
            Profili Düzenle
          </button>
        </div>
      </div>
    </div>

    <!-- 3 Large Teal Action Tiles from Mockup Image 1 -->
    <div class="pt-8 space-y-4">
      <a
        href="/(tabs)/messages"
        class="flex items-center justify-center w-full h-14 rounded-2xl bg-[#00c4b4] hover:bg-[#00a89a] active:scale-[0.99] text-white font-semibold text-lg shadow-sm transition-all"
      >
        Sohbetler
      </a>

      <a
        href="/(tabs)/feed"
        class="flex items-center justify-center w-full h-14 rounded-2xl bg-[#00c4b4] hover:bg-[#00a89a] active:scale-[0.99] text-white font-semibold text-lg shadow-sm transition-all"
      >
        Paylaşımlar
      </a>

      <div
        class="flex items-center justify-center w-full h-14 rounded-2xl bg-[#00c4b4] text-white font-semibold text-lg shadow-sm"
      >
        Puan
      </div>
    </div>
  </div>

  <footer class="py-4 text-center text-xs text-muted-foreground/60">
    <span>EtkinlikCepte • {t('nav.profile')}</span>
  </footer>
</div>
