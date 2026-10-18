<!--
  @component TabsLayout
  @desc Main application tab shell featuring the floating rounded navigation bar matching the UI mockups.
  Props:
    - children: Snippet - Page content for the active tab
  Events: None
-->
<script lang="ts">
  import { page } from '$app/state';
  import { t } from '$lib/i18n.js';
  import {
    CalendarDays,
    Search,
    Building2,
    Heart,
    Settings,
    MessageSquare,
    Bell,
  } from '@lucide/svelte';

  let { children } = $props();

  const tabs = [
    { href: '/(tabs)/discover', label: 'Keşfet', icon: CalendarDays },
    { href: '/(tabs)/feed', label: 'Ara', icon: Search },
    { href: '/(tabs)/clubs', label: 'Mekanlar', icon: Building2 },
    { href: '/(tabs)/tickets', label: 'Kaydedilenler', icon: Heart },
    { href: '/(tabs)/profile', label: 'Ayarlar', icon: Settings },
  ];

  function isActive(href: string): boolean {
    return page.url.pathname === href || page.url.pathname.startsWith(href + '/');
  }
</script>

<div class="flex flex-col min-h-screen">
  <!-- Top App Bar -->
  <header
    class="sticky top-0 z-40 w-full bg-background/90 backdrop-blur-md px-5 h-14 flex items-center justify-between border-b border-border/40"
  >
    <a
      href="/"
      class="font-extrabold text-xl tracking-tight text-primary flex items-center gap-1.5"
    >
      <span>keşfet.</span>
    </a>
    <div class="flex items-center gap-2">
      <a
        href="/(tabs)/messages"
        aria-label={t('nav.messages')}
        class="w-10 h-10 rounded-full bg-white dark:bg-card border border-border/60 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
      >
        <MessageSquare class="w-4 h-4" />
      </a>
      <a
        href="/notifications"
        aria-label={t('nav.notifications')}
        class="w-10 h-10 rounded-full bg-white dark:bg-card border border-border/60 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
      >
        <Bell class="w-4 h-4" />
      </a>
    </div>
  </header>

  <!-- Tab Page Content -->
  <main class="flex-1 pb-24">
    {@render children()}
  </main>

  <!-- Floating Rounded Bottom Navigation Bar from UI Mockups -->
  <div class="fixed bottom-3 left-4 right-4 z-40 max-w-sm mx-auto">
    <nav
      class="bg-white/95 dark:bg-card/95 backdrop-blur-md border border-border/80 shadow-lg rounded-3xl px-2 py-1.5 flex items-center justify-around"
    >
      {#each tabs as tab}
        {@const active = isActive(tab.href)}
        {@const Icon = tab.icon}
        <a
          href={tab.href}
          class="flex flex-col items-center justify-center flex-1 py-1 px-1 rounded-2xl transition-all {active
            ? 'bg-[#fef2e8] dark:bg-[#2a221b] text-[#ea580c] font-semibold'
            : 'text-muted-foreground hover:text-foreground'}"
        >
          <span class="text-[10px] tracking-tight leading-tight mb-0.5">{tab.label}</span>
          <Icon
            class="w-5 h-5 {active ? 'text-[#ea580c]' : 'text-foreground/70'}"
            strokeWidth={active ? 2.2 : 1.8}
          />
        </a>
      {/each}
    </nav>
  </div>
</div>
