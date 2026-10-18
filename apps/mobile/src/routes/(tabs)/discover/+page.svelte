<!--
  @component DiscoverPage
  @desc Main event discovery screen matching UI mockup Image 6.
  Props: None
  Events: None
-->
<script lang="ts">
  import {
    MapPin,
    ChevronDown,
    Moon,
    Sparkles,
    Clock,
    Calendar,
    Heart,
    ArrowUpRight,
    ArrowRight,
  } from '@lucide/svelte';

  const filterChips = [
    { label: 'Bu gece', icon: Moon, active: true },
    { label: 'Hafta sonu', icon: Sparkles, active: false },
    { label: 'Bu hafta', icon: Clock, active: false },
    { label: 'Tarih seç', icon: Calendar, active: false },
  ];

  const popularEvents = [
    {
      id: 'taksirat',
      title: 'Taksirat Festival',
      date: 'Aralık 6, 2026 • Konum',
      image:
        'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=300&q=80',
    },
    {
      id: 'igor',
      title: 'Igor Djambazov na Ohridski',
      date: 'Aralık 6, 2026 • Konum',
      image:
        'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=300&q=80',
    },
  ];
</script>

<div class="px-5 py-4 space-y-6 max-w-sm mx-auto">
  <!-- Top Header with Brand & Location Picker -->
  <div class="flex items-center justify-between">
    <span class="text-xl font-black text-[#ea580c] tracking-tight">keşfet.</span>
    <button
      type="button"
      class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white dark:bg-card border border-border/80 text-xs font-medium text-foreground shadow-xs hover:bg-muted/40 transition-colors cursor-pointer"
    >
      <MapPin class="w-3.5 h-3.5 text-[#ea580c]" />
      <span>Bitola</span>
      <ChevronDown class="w-3 h-3 text-muted-foreground" />
    </button>
  </div>

  <!-- Page Headline -->
  <div>
    <h1 class="text-2xl font-extrabold tracking-tight text-foreground leading-snug">
      Yakındaki Etkinlikleri<br />Keşfet
    </h1>
  </div>

  <!-- Filter Chips Row (Mockup 6) -->
  <div class="grid grid-cols-4 gap-2">
    {#each filterChips as chip}
      {@const Icon = chip.icon}
      <button
        type="button"
        class="flex flex-col items-center justify-center p-2.5 rounded-2xl border text-center transition-all cursor-pointer {chip.active
          ? 'bg-[#fef2e8] dark:bg-[#2a221b] border-[#fed7aa] text-[#ea580c] shadow-xs'
          : 'bg-white dark:bg-card border-border/80 text-muted-foreground hover:border-[#ea580c]/30'}"
      >
        <Icon class="w-4 h-4 mb-1.5 {chip.active ? 'text-[#ea580c]' : 'text-foreground/70'}" />
        <span class="text-[11px] font-semibold leading-tight">{chip.label}</span>
      </button>
    {/each}
  </div>

  <!-- Featured Event Hero Card (Mockup 6) -->
  <div class="relative rounded-3xl overflow-hidden shadow-md group">
    <a href="/events/galija-bitola" class="block relative aspect-[4/3] w-full">
      <!-- Background Image -->
      <img
        src="https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80"
        alt="Galija - Bitola"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      <!-- Gradient Overlay -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-black/20"></div>

      <!-- Top Badges -->
      <div class="absolute top-4 left-4 right-4 flex items-center justify-between">
        <span
          class="px-3 py-1 rounded-xl bg-[#ef4444] text-white font-bold text-[11px] tracking-wider uppercase shadow-xs"
        >
          POPULAR
        </span>
        <button
          type="button"
          aria-label="Beğen"
          class="w-9 h-9 rounded-full bg-white/90 backdrop-blur-xs flex items-center justify-center text-[#ef4444] shadow-xs hover:bg-white transition-colors cursor-pointer"
          onclick={(e) => {
            e.preventDefault();
            e.stopPropagation();
          }}
        >
          <Heart class="w-4 h-4 fill-current" />
        </button>
      </div>

      <!-- Bottom Card Info -->
      <div class="absolute bottom-4 left-4 right-4 flex items-end justify-between">
        <div class="space-y-1 text-white pr-2">
          <h2 class="text-xl font-bold tracking-tight leading-tight drop-shadow-sm">
            Galija - Bitola
          </h2>
          <div class="flex items-center gap-1.5 text-xs text-white/90">
            <MapPin class="w-3.5 h-3.5 text-white/80" />
            <span>Rakometno Igralishte</span>
          </div>
          <div class="flex items-center gap-1.5 text-xs text-white/80">
            <Calendar class="w-3.5 h-3.5 text-white/80" />
            <span>Jul 18, 2026 • 18:00</span>
          </div>
        </div>

        <!-- Orange Arrow Button -->
        <div
          class="w-11 h-11 rounded-full bg-[#ea580c] flex items-center justify-center text-white shadow-md group-hover:bg-[#c2410c] transition-colors shrink-0"
        >
          <ArrowUpRight class="w-5 h-5 stroke-[2.5]" />
        </div>
      </div>
    </a>
  </div>

  <!-- Popüler Etkinlikler Section -->
  <div class="space-y-3 pt-1">
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-foreground">Popüler Etkinlikler</h2>
      <a
        href="/(tabs)/feed"
        aria-label="Tümünü gör"
        class="w-7 h-7 rounded-full bg-[#ef4444] flex items-center justify-center text-white shadow-xs hover:bg-[#dc2626] transition-colors"
      >
        <ArrowRight class="w-3.5 h-3.5" />
      </a>
    </div>

    <!-- Event List -->
    <div class="space-y-3">
      {#each popularEvents as item}
        <a
          href="/events/{item.id}"
          class="flex items-center justify-between p-3 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-[#ea580c]/30 hover:shadow-sm transition-all"
        >
          <div class="flex items-center gap-3">
            <img
              src={item.image}
              alt={item.title}
              class="w-14 h-14 rounded-xl object-cover shrink-0"
            />
            <div class="space-y-0.5">
              <h3 class="text-sm font-bold text-foreground leading-snug line-clamp-1">
                {item.title}
              </h3>
              <p class="text-xs text-muted-foreground">{item.date}</p>
            </div>
          </div>
          <button
            type="button"
            aria-label="Favori"
            class="p-2 text-muted-foreground hover:text-[#ef4444] transition-colors cursor-pointer"
            onclick={(e) => {
              e.preventDefault();
              e.stopPropagation();
            }}
          >
            <Heart class="w-4 h-4 text-[#ef4444]" />
          </button>
        </a>
      {/each}
    </div>
  </div>
</div>
