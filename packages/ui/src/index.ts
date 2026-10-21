/**
 * @etkinlikcepte/ui — Shared design system & UI primitives (§5, §3.1).
 *
 * Invariants (§5.1):
 * - No network requests, tokens, or routing information allowed in this package.
 * - Pure UI behavior, presentation, and accessible primitives.
 */

export { cn } from './lib/utils.js';
export { default as Button } from './lib/components/ui/button.svelte';
export { default as Card } from './lib/components/ui/card.svelte';
