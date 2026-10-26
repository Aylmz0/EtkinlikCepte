/**
 * Offline read model (H2.13).
 *
 * Tauri builds use the SQL plugin with WAL; the browser fallback keeps the
 * same API on localStorage so web E2E and development still work.
 */
type CacheRow = { key: string; value: string; updated_at: string };

const PREFIX = 'etkinlikcepte.cache.';
let sqlite: { execute: (sql: string, params?: unknown[]) => Promise<unknown>; select: <T>(sql: string, params?: unknown[]) => Promise<T> } | null = null;

async function getSqlite() {
  if (sqlite) return sqlite;
  if (typeof window === 'undefined' || !('__TAURI_INTERNALS__' in window)) return null;
  const { default: Database } = await import('@tauri-apps/plugin-sql');
  const db = await Database.load('sqlite:etkinlikcepte.db');
  await db.execute('PRAGMA journal_mode=WAL');
  await db.execute(
    'CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TEXT NOT NULL)'
  );
  sqlite = db;
  return db;
}

export async function cacheSet(key: string, value: unknown): Promise<void> {
  const row: CacheRow = {
    key,
    value: JSON.stringify(value),
    updated_at: new Date().toISOString()
  };
  const db = await getSqlite();
  if (db) {
    await db.execute(
      'INSERT INTO cache (key, value, updated_at) VALUES ($1, $2, $3) ON CONFLICT(key) DO UPDATE SET value=$2, updated_at=$3',
      [row.key, row.value, row.updated_at]
    );
    return;
  }
  if (typeof window !== 'undefined') window.localStorage.setItem(PREFIX + key, row.value);
}

export async function cacheGet<T>(key: string): Promise<T | null> {
  const db = await getSqlite();
  if (db) {
    const rows = await db.select<{ value: string }[]>('SELECT value FROM cache WHERE key = $1', [key]);
    return rows[0] ? (JSON.parse(rows[0].value) as T) : null;
  }
  if (typeof window === 'undefined') return null;
  const raw = window.localStorage.getItem(PREFIX + key);
  return raw ? (JSON.parse(raw) as T) : null;
}
