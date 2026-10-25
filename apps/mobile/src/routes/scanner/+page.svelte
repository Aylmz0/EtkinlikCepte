<!--
  @component ScannerPage
  @desc QR code door validation scanner (§1.6, Owners: P2, P7). The camera feed
    and QR decode/verify call are backend-dependent and not wired here; this
    screen only prepares the frame and the manual-entry fallback UI.
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, ScanLine, Keyboard } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  let manualEntry = $state(false);
  let manualCode = $state('');
</script>

<div class="min-h-screen bg-[#121214] text-white flex flex-col px-6 py-8 max-w-sm mx-auto">
  <div class="flex items-center justify-between">
    <a
      href="/scanner"
      onclick={(e) => {
        e.preventDefault();
        history.back();
      }}
      aria-label={t('common.back')}
      class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center text-white/80 hover:text-white transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-sm font-semibold text-white/90">{t('scanner.title')}</h1>
    <div class="w-10"></div>
  </div>

  <div class="flex-1 flex flex-col items-center justify-center gap-6">
    <div class="relative w-64 h-64 rounded-3xl border border-white/15 overflow-hidden">
      <div class="absolute inset-0 bg-white/5"></div>
      {#each ['top-3 left-3 border-t-2 border-l-2', 'top-3 right-3 border-t-2 border-r-2', 'bottom-3 left-3 border-b-2 border-l-2', 'bottom-3 right-3 border-b-2 border-r-2'] as corner}
        <div class="absolute {corner} w-8 h-8 border-[#ea580c] rounded-sm"></div>
      {/each}
      <ScanLine class="absolute inset-0 m-auto w-10 h-10 text-[#ea580c]/60" />
    </div>
    <p class="text-xs text-white/60 text-center max-w-[220px]">
      {t('scanner.instructions')}
    </p>
  </div>

  <div class="space-y-3 pb-4">
    {#if manualEntry}
      <input
        type="text"
        bind:value={manualCode}
        placeholder={t('scanner.code_placeholder')}
        class="w-full h-12 px-4 rounded-2xl bg-white/10 border border-white/15 text-white placeholder:text-white/40 text-sm focus:outline-none focus:ring-2 focus:ring-[#ea580c]/50 transition-all"
      />
    {/if}
    <button
      type="button"
      onclick={() => (manualEntry = !manualEntry)}
      class="w-full h-12 rounded-2xl bg-white/10 hover:bg-white/15 text-white text-sm font-semibold flex items-center justify-center gap-2 transition-colors cursor-pointer"
    >
      <Keyboard class="w-4 h-4" />
      <span>{manualEntry ? t('scanner.back_to_scan') : t('scanner.manual_entry')}</span>
    </button>
  </div>
</div>
