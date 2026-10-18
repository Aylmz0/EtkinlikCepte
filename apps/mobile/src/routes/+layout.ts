/**
 * SvelteKit Mobile Shell Layout Settings (§4.11).
 *
 * Hard Invariants:
 * - `ssr = false`: Pure client-side SPA embedded in Tauri webview.
 * - `prerender = false`: Routes are dynamic and rendered on device.
 */
export const ssr = false;
export const prerender = false;
export const trailingSlash = 'never';
