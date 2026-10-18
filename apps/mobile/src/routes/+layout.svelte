<!--
  @component RootLayout
  @desc Root layout component providing base styling and dark mode initialization.
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
  class="min-h-screen bg-background text-foreground antialiased selection:bg-primary selection:text-primary-foreground font-sans"
>
  {@render children()}
</div>
