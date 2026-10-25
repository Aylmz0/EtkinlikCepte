/**
 * Minimal translation helper for the mobile shell.
 *
 * The Turkish catalogue is the primary source (§6.2); English lives beside it.
 * Keys are dotted paths (`nav.discover`). Missing keys fall back to the key
 * itself so a missing translation is visible during development instead of
 * silently rendering an empty string. The active catalogue follows
 * `preferences.locale` so switching language in Settings updates every `t()`
 * call reactively.
 */
import tr from '../locales/tr.json';
import en from '../locales/en.json';
import { preferences } from './preferences.svelte.js';

/** @type {Record<string, Record<string, unknown>>} */
const catalogues = { tr, en };

/**
 * Resolve a dotted translation key against the active locale catalogue.
 *
 * @param {string} key Dotted key, for example `nav.discover`.
 * @returns {string} Translated string, or the key when it is missing.
 */
export function t(key) {
  const messages = catalogues[preferences.locale];
  const value = key
    .split('.')
    .reduce(
      (node, part) =>
        node && typeof node === 'object'
          ? /** @type {Record<string, unknown>} */ (node)[part]
          : undefined,
      /** @type {unknown} */ (messages),
    );
  return typeof value === 'string' ? value : key;
}
