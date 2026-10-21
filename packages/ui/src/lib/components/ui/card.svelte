<!--
  @component Card
  @desc Surface container used by app screens. Props: class, children.
  Events: none.
-->
<script lang="ts">
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils.js';

  let { class: className = '', children }: { class?: string; children: Snippet } = $props();
</script>

<div class={cn('rounded-xl border border-border bg-card text-card-foreground shadow-sm', className)}>
  {@render children()}
</div>
