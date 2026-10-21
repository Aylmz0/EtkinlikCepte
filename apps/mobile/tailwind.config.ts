import type { Config } from 'tailwindcss';

/**
 * Tailwind configuration maintained strictly for IDE IntelliSense (§5, H1.13).
 * Runtime styling is driven by CSS-first @theme rules defined in packages/ui/src/tokens.css.
 */
export default {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    '../../packages/ui/src/**/*.{html,js,svelte,ts}'
  ],
  darkMode: 'class',
  theme: {
    extend: {}
  },
  plugins: []
} satisfies Config;
