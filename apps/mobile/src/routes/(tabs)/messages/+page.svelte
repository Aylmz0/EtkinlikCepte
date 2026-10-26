<!--
  @component MessagesPage
  @desc Direct messages conversation list (§1.6). Modernized into chat-app
    style rows: avatar with online dot, last-message preview, and an unread
    badge, instead of a flat name/date bar.
  Props: None
  Events: None
-->
<script lang="ts">
  import { Search, Plus, Trash2 } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { conversations, removeConversation } from '$lib/conversations.svelte.js';
  import { clickOutside } from '@etkinlikcepte/ui';

  let contextMenu = $state<{ id: string; x: number; y: number } | null>(null);

  function openContextMenu(e: MouseEvent, id: string) {
    e.preventDefault();
    contextMenu = { id, x: e.clientX, y: e.clientY };
  }

  function deleteConversation() {
    if (!contextMenu) return;
    removeConversation(contextMenu.id);
    contextMenu = null;
  }
</script>

<div class="px-5 py-4 space-y-5 max-w-sm mx-auto">
  <!-- Title -->
  <div class="pt-2 text-center">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">{t('messages.title')}</h1>
  </div>

  <!-- Search Bar -->
  <div class="relative">
    <div class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none">
      <Search class="w-4 h-4" />
    </div>
    <input
      type="text"
      placeholder={t('messages.search_placeholder')}
      class="w-full h-12 pl-11 pr-4 rounded-2xl border border-border/70 bg-white dark:bg-card text-sm placeholder:text-muted-foreground/60 shadow-xs focus:outline-none focus:ring-2 focus:ring-[#ea580c]/30 focus:border-[#ea580c] transition-all"
    />
  </div>

  <!-- Conversation List -->
  <div class="space-y-2.5">
    {#each conversations as conv (conv.id)}
      <a
        href="/channels/{conv.id}"
        oncontextmenu={(e) => openContextMenu(e, conv.id)}
        class="flex items-center gap-3 p-3 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-[#ea580c]/30 hover:shadow-sm transition-all"
      >
        <!-- Avatar + online dot -->
        <div class="relative shrink-0">
          <div
            class="w-12 h-12 rounded-full bg-[#dcfce7] dark:bg-[#1e3a2f] flex items-center justify-center shadow-xs"
          >
            <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400 select-none">
              {conv.name.slice(0, 2).toUpperCase()}
            </span>
          </div>
          {#if conv.online}
            <span
              class="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-emerald-500 border-2 border-background"
            ></span>
          {/if}
        </div>

        <!-- Name + last message -->
        <div class="flex-1 min-w-0 space-y-0.5">
          <h3 class="text-sm font-bold text-foreground leading-snug line-clamp-1">
            {conv.name}
          </h3>
          <p
            class="text-xs leading-snug line-clamp-1 {conv.unread > 0
              ? 'text-foreground font-medium'
              : 'text-muted-foreground'}"
          >
            {conv.lastMessage}
          </p>
        </div>

        <!-- Time + unread badge -->
        <div class="flex flex-col items-end gap-1 shrink-0">
          <span class="text-[11px] text-muted-foreground">{conv.time}</span>
          {#if conv.unread > 0}
            <span
              class="min-w-[18px] h-[18px] px-1 rounded-full bg-primary text-primary-foreground text-[10px] font-bold flex items-center justify-center"
            >
              {conv.unread}
            </span>
          {/if}
        </div>
      </a>
    {/each}
  </div>
</div>

<a
  href="/messages/new"
  aria-label={t('messages.new_chat')}
  class="fixed bottom-24 right-4 z-30 w-14 h-14 rounded-full bg-primary text-primary-foreground shadow-lg flex items-center justify-center hover:bg-[#dc2626] active:scale-95 transition-all"
>
  <Plus class="w-6 h-6" />
</a>

{#if contextMenu}
  <div
    class="fixed z-50 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-lg py-1.5 min-w-[140px]"
    style="left: {contextMenu.x}px; top: {contextMenu.y}px;"
    use:clickOutside={() => (contextMenu = null)}
  >
    <button
      type="button"
      onclick={deleteConversation}
      class="w-full flex items-center gap-2 px-3.5 py-2 text-left text-xs font-semibold text-destructive hover:bg-destructive/10 transition-colors cursor-pointer"
    >
      <Trash2 class="w-3.5 h-3.5" />
      {t('messages.delete_chat')}
    </button>
  </div>
{/if}
