<!--
  @component Button
  @desc shadcn-svelte-style button primitive. Props: variant, class, children.
  Events: native button events are forwarded through `restProps`.
-->
<script lang="ts">
  import type { Snippet } from 'svelte';
  import { cn } from '../../utils.js';

  type Variant = 'default' | 'outline' | 'ghost';

  let {
    variant = 'default',
    class: className = '',
    children,
  }: { variant?: Variant; class?: string; children: Snippet } = $props();

  const variants: Record<Variant, string> = {
    default: 'bg-primary text-primary-foreground hover:bg-primary/90',
    outline: 'border border-border bg-background hover:bg-muted',
    ghost: 'hover:bg-muted',
  };
</script>

<button
  class={cn(
    'inline-flex h-10 items-center justify-center rounded-lg px-4 text-sm font-semibold transition-colors focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
    variants[variant],
    className,
  )}
>
  {@render children()}
</button>
