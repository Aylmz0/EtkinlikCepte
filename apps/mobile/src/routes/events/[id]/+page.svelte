<!--
  @component EventDetailPage
  @desc Event details screen matching UI mockups Images 8 and 10.
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, Share2, Heart, MapPin, ArrowUpRight } from '@lucide/svelte';
</script>

<div
  class="min-h-screen bg-gradient-to-b from-[#fbf7f2] via-[#f8f2eb] to-[#fbf7f2] dark:from-[#121214] dark:to-[#18181b] pb-28"
>
  <!-- Top Hero Banner Image (Mockups 8 & 10) -->
  <div
    class="relative w-full aspect-[4/3.8] max-w-md mx-auto rounded-b-[2.5rem] overflow-hidden shadow-md"
  >
    <img
      src="https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=1000&q=80"
      alt="Galija - Bitola"
      class="w-full h-full object-cover"
    />
    <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/25 to-black/30"></div>

    <!-- Floating Top Action Buttons -->
    <div class="absolute top-5 left-5 right-5 flex items-center justify-between z-10">
      <a
        href="/(tabs)/discover"
        aria-label="Geri"
        class="w-10 h-10 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center text-foreground shadow-sm hover:bg-white transition-colors"
      >
        <ArrowLeft class="w-4 h-4 text-[#ef4444]" />
      </a>

      <div class="flex items-center gap-2.5">
        <button
          type="button"
          aria-label="Paylaş"
          class="w-10 h-10 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center text-[#ef4444] shadow-sm hover:bg-white transition-colors cursor-pointer"
        >
          <Share2 class="w-4 h-4" />
        </button>
        <button
          type="button"
          aria-label="Favori"
          class="w-10 h-10 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center text-[#ef4444] shadow-sm hover:bg-white transition-colors cursor-pointer"
        >
          <Heart class="w-4 h-4" />
        </button>
      </div>
    </div>

    <!-- Title and Date Badge Overlay at bottom of hero -->
    <div class="absolute bottom-5 left-5 right-5 flex items-end justify-between z-10">
      <div class="space-y-1 text-white pr-3">
        <h1 class="text-2xl font-black tracking-tight drop-shadow-sm">Galija - Bitola</h1>
        <div class="flex items-center gap-1.5 text-xs text-white/90">
          <MapPin class="w-3.5 h-3.5 text-white/80" />
          <span>Rakometno Igralishte</span>
        </div>
      </div>

      <!-- White Date Badge: 17 TEM -->
      <div class="w-14 py-2 px-1 rounded-2xl bg-white text-center shadow-md shrink-0">
        <span class="block text-xl font-black text-[#ef4444] leading-tight">17</span>
        <span class="block text-[10px] font-extrabold text-[#ef4444] tracking-wider uppercase"
          >TEM</span
        >
      </div>
    </div>
  </div>

  <!-- Content Body: Etkinlik Hakkında Card -->
  <main class="px-5 pt-6 max-w-sm mx-auto space-y-4">
    <div class="rounded-3xl bg-white dark:bg-card border border-border/80 p-5 shadow-xs space-y-4">
      <h2 class="text-lg font-bold text-foreground">Etkinlik Hakkında</h2>
      <p class="text-xs text-muted-foreground leading-relaxed">
        Bu eşsiz konserde, sevilen grup Galija en popüler şarkılarıyla sahne alıyor. Harika bir
        atmosferde müzik dolu unutulmaz bir geceye davetlisiniz.
      </p>
      <div class="pt-2 border-t border-border/60">
        <span class="text-sm font-bold text-foreground">Fiyat: 600 MKD</span>
      </div>
    </div>
  </main>

  <!-- Sticky Bottom Floating Action Bar (Mockups 8 & 10) -->
  <div class="fixed bottom-4 left-4 right-4 z-40 max-w-sm mx-auto">
    <div
      class="bg-white/95 dark:bg-card/95 backdrop-blur-md border border-border/80 shadow-lg rounded-3xl px-5 py-3 flex items-center justify-between"
    >
      <div class="space-y-0.5">
        <span class="block text-[10px] font-bold text-muted-foreground uppercase tracking-wider"
          >FİYAT</span
        >
        <span class="text-base font-black text-foreground">600 MKD</span>
      </div>

      <a
        href="/events/1/tickets"
        class="h-11 px-6 rounded-2xl bg-[#ef4444] hover:bg-[#dc2626] text-white text-sm font-bold flex items-center gap-1.5 shadow-sm active:scale-[0.98] transition-all"
      >
        <span>Bilet Al</span>
        <ArrowUpRight class="w-4 h-4 stroke-[2.5]" />
      </a>
    </div>
  </div>
</div>
