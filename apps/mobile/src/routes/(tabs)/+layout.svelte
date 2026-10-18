<!--
  @component TabsLayout
  @desc Main application tab shell featuring top bar and bottom navigation bar (§1.5).
  Props:
    - children: Snippet - Page content for the active tab
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';

  let { children } = $props();

  const tabs = [
    { href: '/(tabs)/discover', labelKey: 'nav.discover' },
    { href: '/(tabs)/feed', labelKey: 'nav.feed' },
    { href: '/(tabs)/clubs', labelKey: 'nav.clubs' },
    { href: '/(tabs)/tickets', labelKey: 'nav.tickets' },
    { href: '/(tabs)/profile', labelKey: 'nav.profile' },
  ];
</script>

<div class="flex flex-col min-h-screen">
  <!-- Top Bar -->
  <header
    class="sticky top-0 z-40 w-full border-b border-border bg-background/95 backdrop-blur px-4 h-14 flex items-center justify-between"
  >
    <a href="/" class="font-bold text-lg text-primary tracking-tight">
      {t('app.name')}
    </a>
    <div class="flex items-center gap-2">
      <a
        href="/(tabs)/messages"
        aria-label={t('nav.messages')}
        class="min-h-[44px] min-w-[44px] inline-flex items-center justify-center rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
      >
        <span class="text-xs font-medium">{t('nav.messages')}</span>
      </a>
      <a
        href="/notifications"
        aria-label={t('nav.notifications')}
        class="min-h-[44px] min-w-[44px] inline-flex items-center justify-center rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
      >
        <span class="text-xs font-medium">{t('nav.notifications')}</span>
      </a>
    </div>
  </header>

  <!-- Tab Content -->
  <main class="flex-1 pb-20">
    {@render children()}
  </main>

  <!-- Bottom Navigation Bar (min 44px touch targets §16) -->
  <nav
    class="fixed bottom-0 left-0 right-0 z-40 border-t border-border bg-background/95 backdrop-blur px-2 h-16 flex items-center justify-around"
  >
    {#each tabs as tab}
      <a
        href={tab.href}
        class="flex flex-col items-center justify-center flex-1 h-full min-h-[44px] min-w-[44px] text-muted-foreground hover:text-primary transition-colors"
      >
        <span class="text-xs font-medium">{t(tab.labelKey)}</span>
      </a>
    {/each}
  </nav>
</div>
