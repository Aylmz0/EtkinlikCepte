<!--
  @component NewChatPage
  @desc Start a new direct message conversation by contact name (§1.6).
    Frontend-only: the conversation is added to local app state (and shows
    up immediately in Mesajlar), it is not sent to a backend.
  Props: None
  Events: None
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { ArrowLeft, MessageSquarePlus } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { addConversation } from '$lib/conversations.svelte.js';

  let name = $state('');

  function submit(e: Event) {
    e.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) return;
    const created = addConversation(trimmed);
    goto(`/channels/${created.id}`);
  }
</script>

<div class="min-h-screen px-6 py-8 max-w-sm mx-auto space-y-8">
  <div class="flex items-center gap-3">
    <a
      href="/messages"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('messages.new_chat')}</h1>
  </div>

  <div class="flex flex-col items-center text-center gap-3 pt-2">
    <div
      class="w-16 h-16 rounded-full bg-[#fef2e8] dark:bg-[#2a221b] flex items-center justify-center text-[#ea580c]"
    >
      <MessageSquarePlus class="w-7 h-7" />
    </div>
    <p class="text-xs text-muted-foreground max-w-[240px]">
      {t('messages.new_chat_hint')}
    </p>
  </div>

  <form class="space-y-5" onsubmit={submit}>
    <div class="space-y-1.5">
      <label for="contact-name" class="text-xs font-medium text-foreground/80"
        >{t('messages.contact_name_label')}</label
      >
      <!-- svelte-ignore a11y_autofocus -- opening this screen should raise the keyboard immediately, consistent with the chat composer -->
      <input
        id="contact-name"
        type="text"
        bind:value={name}
        placeholder={t('messages.contact_name_placeholder')}
        autofocus
        class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
      />
    </div>

    <button
      type="submit"
      disabled={!name.trim()}
      class="w-full h-12 rounded-2xl font-semibold text-sm shadow-sm transition-all {name.trim()
        ? 'bg-primary text-primary-foreground hover:bg-[#dc2626] active:scale-[0.99] cursor-pointer'
        : 'bg-primary/40 text-primary-foreground cursor-not-allowed'}"
    >
      {t('messages.continue')}
    </button>
  </form>
</div>
