<!--
  @component SearchPage
  @desc Search and filtering screen matching UI mockup Image 7.
  Props: None
  Events: None
-->
<script lang="ts">
  import { Search, SlidersHorizontal, Heart, MapPin, ArrowUpRight } from '@lucide/svelte';

  const recentSearches = [
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
    {
      id: 'beer-fest',
      title: 'Beer Festival Skopje',
      date: 'Aralık 6, 2026 • Konum',
      image:
        'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=300&q=80',
    },
  ];
</script>

<div class="px-5 py-4 space-y-5 max-w-sm mx-auto">
  <!-- Header: Ara & Brand -->
  <div class="flex items-center justify-between pt-1">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">Ara</h1>
    <span class="text-xl font-black text-[#ea580c] tracking-tight">keşfet.</span>
  </div>

  <!-- Search Input + Orange Filter Button (Mockup 7) -->
  <div class="flex items-center gap-2.5">
    <div class="relative flex-1">
      <input
        type="text"
        placeholder="Anahtar kelime ile ara..."
        class="w-full h-12 pl-4 pr-10 rounded-2xl border border-border/80 bg-white dark:bg-card text-sm placeholder:text-muted-foreground/60 shadow-xs focus:outline-none focus:ring-2 focus:ring-[#ea580c]/30 focus:border-[#ea580c] transition-all"
      />
      <div
        class="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"
      >
        <Search class="w-4 h-4" />
      </div>
    </div>

    <button
      type="button"
      class="h-12 px-4 rounded-2xl bg-[#ea580c] hover:bg-[#c2410c] text-white text-xs font-semibold flex items-center gap-1.5 shadow-xs transition-colors shrink-0 cursor-pointer"
    >
      <SlidersHorizontal class="w-3.5 h-3.5" />
      <span>Filtrele</span>
    </button>
  </div>

  <!-- Son İncelenenler Section -->
  <div class="space-y-3 pt-2">
    <h2 class="text-lg font-bold text-foreground">Son İncelenenler</h2>
    <div class="space-y-2.5">
      {#each recentSearches as item}
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

  <!-- Popüler Etkinlikler Featured Card -->
  <div class="space-y-3 pt-2">
    <h2 class="text-lg font-bold text-foreground">Popüler Etkinlikler</h2>

    <div class="relative rounded-3xl overflow-hidden shadow-md group">
      <a href="/events/igor-ohridski" class="block relative aspect-[4/3] w-full">
        <img
          src="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=800&q=80"
          alt="Najdobroto od Igor Djambazov"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-black/20"></div>

        <!-- Badges -->
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

        <!-- Info -->
        <div class="absolute bottom-4 left-4 right-4 flex items-end justify-between">
          <div class="space-y-1 text-white pr-2">
            <h3 class="text-lg font-bold tracking-tight leading-tight drop-shadow-sm">
              Najdobroto od Igor<br />Djambazov na Ohridski
            </h3>
            <div class="flex items-center gap-1.5 text-xs text-white/90">
              <MapPin class="w-3.5 h-3.5 text-white/80" />
              <span>Ancient theater of Ohrid</span>
            </div>
          </div>

          <div
            class="w-11 h-11 rounded-full bg-[#ea580c] flex items-center justify-center text-white shadow-md group-hover:bg-[#c2410c] transition-colors shrink-0"
          >
            <ArrowUpRight class="w-5 h-5 stroke-[2.5]" />
          </div>
        </div>
      </a>
    </div>
  </div>
</div>
