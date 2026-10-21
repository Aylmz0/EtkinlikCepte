/**
 * Minimal translation helper for the mobile shell.
 *
 * The Turkish catalogue is the primary source (§6.2); English lives beside it.
 * Keys are dotted paths (`nav.discover`). Missing keys fall back to the key
 * itself so a missing translation is visible during development instead of
 * silently rendering an empty string.
 */
import tr from '../locales/tr.json';

/** @type {Record<string, unknown>} */
const messages = tr;

/**
 * Resolve a dotted translation key against the Turkish catalogue.
 *
 * @param {string} key Dotted key, for example `nav.discover`.
 * @returns {string} Translated string, or the key when it is missing.
 */
export function t(key) {
  const value = key
    .split('.')
    .reduce(
      (node, part) =>
        node && typeof node === 'object' ? /** @type {Record<string, unknown>} */ (node)[part] : undefined,
      /** @type {unknown} */ (messages)
    );
  return typeof value === 'string' ? value : key;
}
