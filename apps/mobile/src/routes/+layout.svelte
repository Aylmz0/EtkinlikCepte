<!--
  @component RootLayout
  @desc Root layout: warm gradient canvas, reactive theme, the shared app shell
    (top bar + floating bottom navbar) on every screen except auth and
    immersive full-screen routes, and animated route transitions.
  Props:
    - children: Snippet - Rendered child route
  Events: None
-->
<script lang="ts">
  import '@etkinlikcepte/ui/base.css';
  import { page } from '$app/state';
  import { onNavigate } from '$app/navigation';
  import { t } from '$lib/i18n.js';
  import { preferences } from '$lib/preferences.svelte.js';
  import {
    CalendarDays,
    Search,
    Building2,
    Heart,
    User,
    MessageSquare,
    Bell,
  } from '@lucide/svelte';

  let { children } = $props();

  // Routes that own their full screen (landing/auth, camera/call UIs) and
  // must not be wrapped in the tab shell.
  const HIDDEN_SHELL = [
    /^\/$/,
    /^\/login$/,
    /^\/register$/,
    /^\/forgot-password$/,
    /^\/scanner$/,
    /^\/events\/[^/]+\/room$/,
    /^\/channels\/[^/]+\/room$/,
  ];

  let showShell = $derived(!HIDDEN_SHELL.some((pattern) => pattern.test(page.url.pathname)));

  const tabs = [
    { href: '/discover', labelKey: 'nav.discover', icon: CalendarDays },
    { href: '/feed', labelKey: 'nav.feed', icon: Search },
    { href: '/clubs', labelKey: 'nav.clubs', icon: Building2 },
    { href: '/tickets', labelKey: 'nav.tickets', icon: Heart },
    { href: '/profile', labelKey: 'nav.profile', icon: User },
  ];

  function isActive(href: string): boolean {
    return page.url.pathname === href || page.url.pathname.startsWith(href + '/');
  }

  $effect(() => {
    document.documentElement.classList.toggle('dark', preferences.theme === 'dark');
  });

  onNavigate((navigation) => {
    if (!document.startViewTransition) return;
    return new Promise((resolve) => {
      document.startViewTransition(async () => {
        resolve();
        await navigation.complete;
      });
    });
  });
</script>

<div
  class="app-canvas min-h-screen text-foreground antialiased selection:bg-primary selection:text-primary-foreground font-sans"
>
  {#if showShell}
    <div class="flex flex-col min-h-screen">
      <header
        class="sticky top-0 z-40 w-full bg-background/90 backdrop-blur-md px-5 h-14 flex items-center justify-between border-b border-border/40"
      >
        <a
          href="/discover"
          class="font-extrabold text-xl tracking-tight text-primary flex items-center gap-1.5"
        >
          <span>Keşfet.</span>
        </a>
        <div class="flex items-center gap-2">
          <a
            href="/messages"
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

      <main class="flex-1 pb-24">
        {@render children()}
      </main>

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
              <span class="text-[10px] tracking-tight leading-tight mb-0.5">{t(tab.labelKey)}</span>
              <Icon
                class="w-5 h-5 {active ? 'text-[#ea580c]' : 'text-foreground/70'}"
                strokeWidth={active ? 2.2 : 1.8}
              />
            </a>
          {/each}
        </nav>
      </div>
    </div>
  {:else}
    {@render children()}
  {/if}
</div>
