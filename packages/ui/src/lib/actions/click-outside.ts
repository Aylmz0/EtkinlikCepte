/**
 * Svelte action that calls `onOutside` when a pointer-down lands outside
 * `node`. Used to dismiss popovers (e.g. the Calendar date picker) on an
 * outside click, without a backdrop element.
 *
 * @param node The popover's root element.
 * @param onOutside Called once per outside pointer-down.
 */
export function clickOutside(node: HTMLElement, onOutside: () => void) {
  function handlePointerDown(event: PointerEvent) {
    if (event.target instanceof Node && !node.contains(event.target)) {
      onOutside();
    }
  }

  document.addEventListener('pointerdown', handlePointerDown, true);

  return {
    destroy() {
      document.removeEventListener('pointerdown', handlePointerDown, true);
    },
  };
}
