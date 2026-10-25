<!--
  @component ChatSettingsPage
  @desc Chat appearance preferences — background wallpaper and bubble font
    size apply live to the chat threads; disappearing messages is a saved
    preference (§1.6). Frontend-only: persisted to localStorage, no backend.
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, Check } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import {
    chatSettings,
    setChatBackground,
    setChatFontSize,
    toggleDisappearing,
    CHAT_BACKGROUND_CLASSES,
    type ChatBackground,
    type ChatFontSize,
  } from '$lib/chatSettings.svelte.js';

  const backgrounds: { id: ChatBackground; labelKey: string }[] = [
    { id: 'default', labelKey: 'chatSettings.bg_default' },
    { id: 'mint', labelKey: 'chatSettings.bg_mint' },
    { id: 'sunset', labelKey: 'chatSettings.bg_sunset' },
    { id: 'midnight', labelKey: 'chatSettings.bg_midnight' },
  ];

  const fontSizes: { id: ChatFontSize; labelKey: string }[] = [
    { id: 'sm', labelKey: 'chatSettings.font_small' },
    { id: 'md', labelKey: 'chatSettings.font_medium' },
    { id: 'lg', labelKey: 'chatSettings.font_large' },
  ];
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto space-y-6 pb-12">
  <div class="flex items-center gap-3 pt-2">
    <a
      href="/settings"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('chatSettings.title')}</h1>
  </div>

  <!-- Background -->
  <div class="space-y-3">
    <h2 class="text-sm font-bold text-foreground">{t('chatSettings.background_label')}</h2>
    <div class="grid grid-cols-4 gap-2.5">
      {#each backgrounds as bg (bg.id)}
        {@const active = chatSettings.background === bg.id}
        <button
          type="button"
          onclick={() => setChatBackground(bg.id)}
          class="space-y-1.5 cursor-pointer"
        >
          <div
            class="aspect-square rounded-2xl border-2 flex items-center justify-center {CHAT_BACKGROUND_CLASSES[
              bg.id
            ]} {active ? 'border-[#ea580c]' : 'border-border/80'}"
          >
            {#if active}
              <div
                class="w-5 h-5 rounded-full bg-[#ea580c] flex items-center justify-center text-white"
              >
                <Check class="w-3 h-3 stroke-[3]" />
              </div>
            {/if}
          </div>
          <span class="block text-[10px] font-medium text-muted-foreground text-center"
            >{t(bg.labelKey)}</span
          >
        </button>
      {/each}
    </div>
  </div>

  <!-- Font size -->
  <div class="space-y-3">
    <h2 class="text-sm font-bold text-foreground">{t('chatSettings.font_size_label')}</h2>
    <div class="grid grid-cols-3 gap-2.5">
      {#each fontSizes as size (size.id)}
        {@const active = chatSettings.fontSize === size.id}
        <button
          type="button"
          onclick={() => setChatFontSize(size.id)}
          class="px-3 py-2.5 rounded-2xl border text-xs font-semibold transition-all cursor-pointer {active
            ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c]'
            : 'bg-white dark:bg-card border-border/80 text-foreground hover:border-[#ea580c]/30'}"
        >
          {t(size.labelKey)}
        </button>
      {/each}
    </div>
  </div>

  <!-- Disappearing messages -->
  <div class="rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs p-4 space-y-1">
    <div class="flex items-center justify-between">
      <span class="text-sm font-medium text-foreground">{t('chatSettings.disappearing_label')}</span
      >
      <button
        type="button"
        role="switch"
        aria-checked={chatSettings.disappearing}
        aria-label={t('chatSettings.disappearing_label')}
        onclick={toggleDisappearing}
        class="w-11 h-6 rounded-full transition-colors cursor-pointer relative shrink-0 {chatSettings.disappearing
          ? 'bg-primary'
          : 'bg-muted'}"
      >
        <span
          class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-transform {chatSettings.disappearing
            ? 'translate-x-5'
            : ''}"
        ></span>
      </button>
    </div>
    <p class="text-[11px] text-muted-foreground leading-relaxed">
      {t('chatSettings.disappearing_hint')}
    </p>
  </div>
</div>
