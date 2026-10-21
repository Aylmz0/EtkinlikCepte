import { defineConfig, devices } from '@playwright/test';

/**
 * Web E2E skeleton (§12). The app is a static SvelteKit build; tests run
 * against the dev server when one is provided, otherwise they stay skipped
 * until the scenario is implemented.
 */
export default defineConfig({
  testDir: './e2e/web',
  fullyParallel: true,
  reporter: 'list',
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:5173',
    trace: 'on-first-retry'
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }]
});
