import type { Config } from 'tailwindcss';

/**
 * IntelliSense-only Tailwind config for the design system (§5, H1.13).
 * Runtime tokens live in `src/tokens.css` via CSS-first @theme.
 */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}', '../../apps/mobile/src/**/*.{html,js,svelte,ts}'],
  darkMode: 'class',
  theme: { extend: {} },
  plugins: []
} satisfies Config;
