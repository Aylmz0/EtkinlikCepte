<!--
  @component ChannelChatPage
  @desc Direct message 1-on-1 private channel (§1.6, Owner: P5). Sending a
    message and starting the live room require the realtime backend; the
    composer submit stays inert while "Canlı Görüşme" only navigates.
  Props: None
  Events: None
-->
<script lang="ts">
  import { page } from '$app/state';
  import { ArrowLeft, Send, Phone } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import {
    chatSettings,
    CHAT_BACKGROUND_CLASSES,
    CHAT_FONT_SIZE_CLASSES,
  } from '$lib/chatSettings.svelte.js';
  import { conversations } from '$lib/conversations.svelte.js';

  let conversation = $derived(
    conversations.find((c) => c.id === page.params.id) ?? conversations[0],
  );

  let draft = $state('');
</script>

<div
  class="{CHAT_BACKGROUND_CLASSES[
    chatSettings.background
  ]} px-5 py-6 pb-28 max-w-sm mx-auto min-h-[calc(100dvh-3.5rem)] flex flex-col"
>
  <div class="flex items-center justify-between gap-3 pt-2 pb-2">
    <div class="flex items-center gap-3">
      <a
        href="/messages"
        aria-label={t('common.back')}
        class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
      >
        <ArrowLeft class="w-4 h-4" />
      </a>
      <h1 class="text-xl font-bold tracking-tight text-foreground">{conversation.name}</h1>
    </div>
    <a
      href="./room"
      aria-label={t('channelChat.start_call')}
      class="w-9 h-9 rounded-full bg-[#00c4b4] text-white flex items-center justify-center shadow-xs hover:bg-[#00a89a] transition-colors"
    >
      <Phone class="w-4 h-4" />
    </a>
  </div>

  <div class="flex-1 space-y-2.5 py-3">
    {#if conversation.thread.length === 0}
      <p class="text-xs text-muted-foreground text-center py-10">{t('messages.empty_thread')}</p>
    {/if}
    {#each conversation.thread as msg (msg.id)}
      <div class="flex {msg.mine ? 'justify-end' : 'justify-start'}">
        <div
          class="max-w-[75%] px-4 py-2.5 rounded-2xl leading-relaxed {CHAT_FONT_SIZE_CLASSES[
            chatSettings.fontSize
          ]} {msg.mine
            ? 'bg-primary text-primary-foreground rounded-br-md'
            : 'bg-[#e0ebf6] dark:bg-[#1e293b] text-foreground rounded-bl-md'}"
        >
          <p>{msg.text}</p>
          <span class="block text-[10px] opacity-70 pt-1">{msg.time}</span>
        </div>
      </div>
    {/each}
  </div>

  <form
    class="fixed bottom-24 left-4 right-4 z-30 max-w-sm mx-auto flex items-center gap-2"
    onsubmit={(e) => e.preventDefault()}
  >
    <!-- svelte-ignore a11y_autofocus -- opening a chat should raise the keyboard immediately, same as WhatsApp/Instagram DMs -->
    <input
      type="text"
      bind:value={draft}
      placeholder={t('channelChat.placeholder')}
      autofocus
      class="flex-1 h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-sm placeholder:text-muted-foreground/60 shadow-lg focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-all"
    />
    <button
      type="submit"
      disabled
      aria-label={t('channelChat.send')}
      class="w-12 h-12 rounded-2xl bg-primary/40 text-primary-foreground flex items-center justify-center shadow-lg cursor-not-allowed"
    >
      <Send class="w-4 h-4" />
    </button>
  </form>
</div>
