<!--
  @component MessagesPage
  @desc Direct messages conversation list matching UI mockup Image 2.
  Props: None
  Events: None
-->
<script lang="ts">
  import { Search } from '@lucide/svelte';

  const conversations = [
    { id: '1', name: 'Kullanıcı adı', date: '26.03.2026' },
    { id: '2', name: 'Kullanıcı adı', date: '23.06.2024' },
    { id: '3', name: 'Kullanıcı adı', date: '26.09.2026' },
    { id: '4', name: 'Kullanıcı adı', date: '31.01.1999' },
    { id: '5', name: 'Kullanıcı adı', date: '06.11.2020' },
  ];
</script>

<div class="px-5 py-4 space-y-6 max-w-sm mx-auto">
  <!-- Centered Title -->
  <div class="pt-2 text-center">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">Mesajlar</h1>
  </div>

  <!-- Search Bar (Mockup 2: "Sohbetlerden ara") -->
  <div class="relative">
    <div class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none">
      <Search class="w-4 h-4" />
    </div>
    <input
      type="text"
      placeholder="Sohbetlerden ara"
      class="w-full h-12 pl-11 pr-4 rounded-2xl border border-border/70 bg-white dark:bg-card text-sm placeholder:text-muted-foreground/60 shadow-xs focus:outline-none focus:ring-2 focus:ring-[#ea580c]/30 focus:border-[#ea580c] transition-all"
    />
  </div>

  <!-- Conversation List (Mockup 2) -->
  <div class="space-y-3.5 pt-1">
    {#each conversations as conv}
      <a href="/channels/{conv.id}" class="flex items-center gap-3 group">
        <!-- Soft Mint Avatar -->
        <div
          class="w-12 h-12 rounded-full bg-[#dcfce7] dark:bg-[#1e3a2f] flex items-center justify-center shrink-0 shadow-xs"
        >
          <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400 select-none">
            {conv.name.slice(0, 2).toUpperCase()}
          </span>
        </div>

        <!-- Soft Light Blue Rounded Item Bar -->
        <div
          class="flex-1 h-12 px-4 rounded-2xl bg-[#e0ebf6] dark:bg-[#1e293b] flex items-center justify-between shadow-xs group-hover:bg-[#d0e2f2] dark:group-hover:bg-[#283548] transition-colors"
        >
          <span class="text-xs font-semibold text-foreground">
            {conv.name}
          </span>
          <span class="text-[11px] text-muted-foreground">
            {conv.date}
          </span>
        </div>
      </a>
    {/each}
  </div>
</div>
