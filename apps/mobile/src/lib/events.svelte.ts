/**
 * Shared mock event catalogue used by Discover and Ara (Search) until the
 * real `/discover` API lands (§1.4). Each event carries enough properties
 * (location, category, price, date) for the quick filters and the Filtreler
 * page to actually narrow the list client-side. Reactive ($state) so an
 * event created on /profile/create-event shows up immediately.
 */

import type { TurkishCity } from './turkishCities.js';

export type EventCategory = 'concert' | 'festival' | 'sport' | 'art';
export type EventPrice = 'free' | 'paid';
export type EventLocation = TurkishCity;

export interface MockEvent {
  id: string;
  title: string;
  venue: string;
  location: EventLocation;
  category: EventCategory;
  price: EventPrice;
  /** ISO date, "YYYY-MM-DD". */
  date: string;
  time: string;
  image: string;
  description: string;
  popular: boolean;
}

function isoDaysFromNow(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

const DEFAULT_DESCRIPTION =
  'Bu eşsiz etkinlikte unutulmaz bir deneyime davetlisiniz. Detaylı bilgi için kulüp sayfasını ziyaret edebilirsiniz.';

/** Built from offsets relative to "today" so the quick filters (tonight,
 * this weekend, this week) always have something to match in demos. */
export const events = $state<MockEvent[]>([
  {
    id: 'galija-bitola',
    title: 'Galija - Bitola',
    venue: 'Rakometno Igralishte',
    location: 'İstanbul',
    category: 'concert',
    price: 'paid',
    date: isoDaysFromNow(0),
    time: '20:00',
    image:
      'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: true,
  },
  {
    id: 'taksirat',
    title: 'Taksirat Festival',
    venue: 'Boris Trajkovski Arena',
    location: 'Ankara',
    category: 'festival',
    price: 'paid',
    date: isoDaysFromNow(2),
    time: '19:30',
    image:
      'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: true,
  },
  {
    id: 'igor',
    title: 'Igor Djambazov na Ohridski',
    venue: 'Ancient Theater of Ohrid',
    location: 'İzmir',
    category: 'concert',
    price: 'paid',
    date: isoDaysFromNow(4),
    time: '21:00',
    image:
      'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: true,
  },
  {
    id: 'beer-fest',
    title: 'Beer Festival Skopje',
    venue: 'Skopje City Park Stage',
    location: 'Ankara',
    category: 'festival',
    price: 'free',
    date: isoDaysFromNow(6),
    time: '17:00',
    image:
      'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'ohrid-run',
    title: 'Ohrid Yarı Maratonu',
    venue: 'Ilindenska',
    location: 'İzmir',
    category: 'sport',
    price: 'free',
    date: isoDaysFromNow(1),
    time: '09:00',
    image:
      'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'mkc-sergi',
    title: 'Çağdaş Sanat Sergisi',
    venue: 'MKC Kültür Merkezi',
    location: 'Ankara',
    category: 'art',
    price: 'free',
    date: isoDaysFromNow(9),
    time: '11:00',
    image:
      'https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'bitola-sokak-turnuvasi',
    title: 'Bitola Sokak Basketbolu',
    venue: 'Rakometno Igralishte',
    location: 'İstanbul',
    category: 'sport',
    price: 'paid',
    date: isoDaysFromNow(5),
    time: '14:00',
    image:
      'https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'istanbul-caz-gecesi',
    title: 'İstanbul Caz Gecesi',
    venue: 'Nardis Jazz Club',
    location: 'İstanbul',
    category: 'concert',
    price: 'paid',
    date: isoDaysFromNow(0),
    time: '21:00',
    image:
      'https://images.unsplash.com/photo-1459749411175-04bf5292ceea?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'kadikoy-sokak-festivali',
    title: 'Kadıköy Sokak Festivali',
    venue: 'Kadıköy Meydan',
    location: 'İstanbul',
    category: 'festival',
    price: 'free',
    date: isoDaysFromNow(0),
    time: '16:00',
    image:
      'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'beyoglu-sanat-gecesi',
    title: 'Beyoğlu Sanat Gecesi',
    venue: 'Pera Sanat Galerisi',
    location: 'İstanbul',
    category: 'art',
    price: 'free',
    date: isoDaysFromNow(0),
    time: '18:00',
    image:
      'https://images.unsplash.com/photo-1531913764164-f85c52e6e654?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'bogazici-kosusu',
    title: 'Boğaziçi Koşusu',
    venue: 'Bebek Sahil',
    location: 'İstanbul',
    category: 'sport',
    price: 'paid',
    date: isoDaysFromNow(0),
    time: '08:00',
    image:
      'https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'akustik-aksam',
    title: 'Akustik Akşam',
    venue: 'Salon İKSV',
    location: 'İstanbul',
    category: 'concert',
    price: 'paid',
    date: isoDaysFromNow(0),
    time: '20:30',
    image:
      'https://images.unsplash.com/photo-1506157786151-b8491531f063?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'elektronik-muzik-partisi',
    title: 'Elektronik Müzik Partisi',
    venue: 'Zorlu PSM',
    location: 'İstanbul',
    category: 'concert',
    price: 'paid',
    date: isoDaysFromNow(0),
    time: '23:00',
    image:
      'https://images.unsplash.com/photo-1485872299829-c673f5194813?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'ankara-rock-gunleri',
    title: 'Ankara Rock Günleri',
    venue: 'Jolly Joker Ankara',
    location: 'Ankara',
    category: 'concert',
    price: 'paid',
    date: isoDaysFromNow(3),
    time: '20:00',
    image:
      'https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'izmir-halk-konseri',
    title: 'İzmir Halk Konseri',
    venue: 'Kültürpark Açıkhava',
    location: 'İzmir',
    category: 'concert',
    price: 'free',
    date: isoDaysFromNow(2),
    time: '19:00',
    image:
      'https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'bursa-tiyatro-festivali',
    title: 'Bursa Tiyatro Festivali',
    venue: 'Merinos AKKM',
    location: 'Bursa',
    category: 'art',
    price: 'paid',
    date: isoDaysFromNow(7),
    time: '19:30',
    image:
      'https://images.unsplash.com/photo-1536924940846-227afb31e2a5?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'antalya-plaj-partisi',
    title: 'Antalya Plaj Partisi',
    venue: 'Konyaaltı Sahili',
    location: 'Antalya',
    category: 'festival',
    price: 'paid',
    date: isoDaysFromNow(10),
    time: '17:00',
    image:
      'https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'eskisehir-bisiklet-turu',
    title: 'Eskişehir Bisiklet Turu',
    venue: 'Porsuk Çayı Kenarı',
    location: 'Eskişehir',
    category: 'sport',
    price: 'free',
    date: isoDaysFromNow(3),
    time: '10:00',
    image:
      'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'mevlana-anma-konseri',
    title: 'Mevlana Anma Konseri',
    venue: 'Mevlana Kültür Merkezi',
    location: 'Konya',
    category: 'concert',
    price: 'free',
    date: isoDaysFromNow(12),
    time: '20:00',
    image:
      'https://images.unsplash.com/photo-1527224857830-43a7acc85260?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'adana-lezzet-festivali',
    title: 'Adana Lezzet Festivali',
    venue: 'Adana Expo Center',
    location: 'Adana',
    category: 'festival',
    price: 'free',
    date: isoDaysFromNow(8),
    time: '12:00',
    image:
      'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
  {
    id: 'trabzon-spor-gunu',
    title: 'Trabzon Spor Günü',
    venue: 'Avni Aker Stadyumu',
    location: 'Trabzon',
    category: 'sport',
    price: 'paid',
    date: isoDaysFromNow(6),
    time: '15:00',
    image:
      'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=800&q=80',
    description: DEFAULT_DESCRIPTION,
    popular: false,
  },
]);

function slugify(title: string): string {
  return title
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

/**
 * Adds a user-created event to the shared catalogue (frontend-only — not
 * sent to a backend). Returns the created event so the caller can navigate
 * to its detail page.
 *
 * @param input Event fields without `id`/`popular`, which are derived here.
 */
export function addEvent(input: Omit<MockEvent, 'id' | 'popular'>): MockEvent {
  const base = slugify(input.title) || 'etkinlik';
  let id = base;
  let suffix = 1;
  while (events.some((e) => e.id === id)) {
    id = `${base}-${++suffix}`;
  }
  const created: MockEvent = { ...input, id, popular: false };
  events.push(created);
  return created;
}

function parseIso(date: string): Date {
  const [y, m, d] = date.split('-').map(Number);
  return new Date(y, m - 1, d);
}

function startOfDay(d: Date): Date {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate());
}

export function isToday(date: string): boolean {
  return date === isoDaysFromNow(0);
}

export function isThisWeek(date: string): boolean {
  const today = startOfDay(new Date());
  const target = startOfDay(parseIso(date));
  const diffDays = Math.round((target.getTime() - today.getTime()) / 86_400_000);
  return diffDays >= 0 && diffDays <= 7;
}

export function isThisWeekend(date: string): boolean {
  const today = startOfDay(new Date());
  const target = startOfDay(parseIso(date));
  const diffDays = Math.round((target.getTime() - today.getTime()) / 86_400_000);
  if (diffDays < 0 || diffDays > 7) return false;
  const day = target.getDay(); // 0 = Sunday, 6 = Saturday
  return day === 0 || day === 6;
}
