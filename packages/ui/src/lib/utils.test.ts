import { describe, expect, it } from 'vitest';
import { cn } from './utils.js';

describe('cn', () => {
  it('merges conflicting tailwind classes', () => {
    expect(cn('px-2', 'px-4')).toBe('px-4');
  });
  it('drops falsey values', () => {
    expect(cn('text-sm', false && 'hidden', undefined)).toBe('text-sm');
  });
});
