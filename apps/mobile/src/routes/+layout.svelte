<!--
  @component RootLayout
  @desc Root layout component providing base styling, warm canvas backdrop, and dark mode initialization.
  Props:
    - children: Snippet - Rendered child route
  Events: None
-->
<script lang="ts">
  import '@etkinlikcepte/ui/base.css';
  import { onMount } from 'svelte';

  let { children } = $props();

  onMount(() => {
    // Detect system dark mode preference if not explicitly set
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.classList.add('dark');
    }
  });
</script>

<div
  class="min-h-screen bg-gradient-to-b from-[#fbf7f2] via-[#f8f2eb] to-[#fbf7f2] dark:from-[#121214] dark:to-[#18181b] text-foreground antialiased selection:bg-primary selection:text-primary-foreground font-sans"
>
  {@render children()}
</div>
