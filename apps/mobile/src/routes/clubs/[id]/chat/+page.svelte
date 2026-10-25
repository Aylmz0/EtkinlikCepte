<!--
  @component ClubChatPage
  @desc Real-time club member group chat (§1.6, Owner: P5). Sending a message
    requires the realtime backend and is not wired here — the composer is
    visually ready but its submit is inert.
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, Send } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  const thread = [
    { id: 1, mine: false, text: 'Bu akşam maç var mı?', time: '19:02' },
    { id: 2, mine: true, text: 'Evet, 20:00’da başlıyor.', time: '19:03' },
    { id: 3, mine: false, text: 'Harika, kapıda görüşürüz!', time: '19:04' },
  ];

  let draft = $state('');
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto flex flex-col pb-4">
  <div class="flex items-center gap-3 pt-2 pb-2">
    <a
      href="../"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-xl font-bold tracking-tight text-foreground">{t('clubChat.title')}</h1>
  </div>

  <div class="flex-1 space-y-2.5 py-3">
    {#each thread as msg (msg.id)}
      <div class="flex {msg.mine ? 'justify-end' : 'justify-start'}">
        <div
          class="max-w-[75%] px-4 py-2.5 rounded-2xl text-xs leading-relaxed {msg.mine
            ? 'bg-primary text-primary-foreground rounded-br-md'
            : 'bg-[#e0ebf6] dark:bg-[#1e293b] text-foreground rounded-bl-md'}"
        >
          <p>{msg.text}</p>
          <span class="block text-[10px] opacity-70 pt-1">{msg.time}</span>
        </div>
      </div>
    {/each}
  </div>

  <form class="flex items-center gap-2 pt-2" onsubmit={(e) => e.preventDefault()}>
    <input
      type="text"
      bind:value={draft}
      placeholder={t('clubChat.placeholder')}
      class="flex-1 h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-sm placeholder:text-muted-foreground/60 shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-all"
    />
    <button
      type="submit"
      disabled
      aria-label={t('clubChat.send')}
      class="w-12 h-12 rounded-2xl bg-primary/40 text-primary-foreground flex items-center justify-center shadow-xs cursor-not-allowed"
    >
      <Send class="w-4 h-4" />
    </button>
  </form>
</div>
