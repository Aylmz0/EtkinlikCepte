/** Class-name helper shared by shadcn-svelte components. */
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge conditional Tailwind classes, letting later classes win.
 *
 * @param inputs Class values accepted by clsx.
 * @returns A single normalized class string.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
