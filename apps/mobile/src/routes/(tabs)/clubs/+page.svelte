<!--
  @component VenuesPage
  @desc Venues screen matching UI mockup Image 9.
  Props: None
  Events: None
-->
<script lang="ts">
  import { MapPin, Search, Star, Heart } from '@lucide/svelte';

  const venues = [
    {
      id: 'ohrid-theater',
      title: 'Ancient Theater of Ohrid',
      address: 'Ilindenska • Ohrid',
      rating: '4.8',
      status: 'Açık',
      category: 'Açık hava tiyatrosu',
      image:
        'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=400&q=80',
    },
    {
      id: 'rakometno',
      title: 'Rakometno Igralishte',
      address: 'Bulevar 1-vi Maj • Bitola',
      rating: '4.7',
      status: 'Açık',
      category: 'Konser alanı',
      image:
        'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=400&q=80',
    },
    {
      id: 'skopje-park',
      title: 'Skopje City Park Stage',
      address: 'Gradski Park • Üsküp',
      rating: '4.9',
      status: 'Açık',
      category: 'Park sahnesi',
      image:
        'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=400&q=80',
    },
    {
      id: 'mkc',
      title: 'MKC Kültür Merkezi',
      address: 'Kej Dimitar Vlahov • Üsküp',
      rating: '4.8',
      status: 'Açık',
      category: 'Kültür ve sanat',
      image:
        'https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=400&q=80',
    },
  ];
</script>

<div class="px-5 py-4 space-y-5 max-w-sm mx-auto">
  <!-- Title and Subtitle -->
  <div class="space-y-1 pt-1">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">Mekanlar</h1>
    <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
      <MapPin class="w-3.5 h-3.5 text-[#ef4444]" />
      <span>Yakınındaki Popüler Mekanlar</span>
    </div>
  </div>

  <!-- Search Input Bar -->
  <div class="relative">
    <div class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none">
      <Search class="w-4 h-4" />
    </div>
    <input
      type="text"
      placeholder="Mekanlarda ara..."
      class="w-full h-12 pl-11 pr-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-sm placeholder:text-muted-foreground/60 shadow-xs focus:outline-none focus:ring-2 focus:ring-[#ea580c]/30 focus:border-[#ea580c] transition-all"
    />
  </div>

  <!-- Section Header -->
  <div class="flex items-center justify-between pt-1">
    <h2 class="text-lg font-bold text-foreground">Öne çıkan mekanlar</h2>
    <span class="text-xs text-muted-foreground">4 mekan</span>
  </div>

  <!-- Venues List (Mockup 9) -->
  <div class="space-y-3">
    {#each venues as venue}
      <a
        href="/clubs/{venue.id}"
        class="flex items-center justify-between p-3.5 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs hover:border-[#ea580c]/40 hover:shadow-sm transition-all"
      >
        <div class="flex items-center gap-3.5">
          <img
            src={venue.image}
            alt={venue.title}
            class="w-18 h-18 rounded-2xl object-cover shrink-0"
          />
          <div class="space-y-1">
            <h3 class="text-sm font-bold text-foreground leading-snug line-clamp-1">
              {venue.title}
            </h3>
            <p class="text-xs text-muted-foreground">{venue.address}</p>
            <div class="flex items-center gap-1.5 text-xs font-semibold text-foreground">
              <Star class="w-3 h-3 text-[#ef4444] fill-current" />
              <span>{venue.rating}</span>
              <span class="text-muted-foreground/40">•</span>
              <span class="text-foreground">{venue.status}</span>
            </div>
            <p class="text-[11px] text-muted-foreground/80">{venue.category}</p>
          </div>
        </div>

        <button
          type="button"
          aria-label="Favorilere ekle"
          class="p-2 text-muted-foreground hover:text-[#ef4444] transition-colors cursor-pointer self-center"
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
