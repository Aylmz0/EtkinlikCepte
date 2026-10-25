<!--
  @component EventDetailPage
  @desc Event details screen matching UI mockups Images 8 and 10. Looks the
    event up from the shared mock catalogue by route id (§1.4). The app does
    not sell tickets (§1.3 non-goals, manual-approval only) — no purchase CTA.
  Props: None
  Events: None
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/state';
  import { ArrowLeft, Share2, Heart, MapPin, Calendar, MessageCircle } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';
  import { events } from '$lib/events.svelte.js';
  import { findOrCreateConversation } from '$lib/conversations.svelte.js';

  let event = $derived(events.find((e) => e.id === page.params.id) ?? events[0]);

  // Frontend-only favorite toggle (no backend sync).
  let favorited = $state(false);

  function messageOrganizer() {
    const conversation = findOrCreateConversation(event.venue);
    goto(`/channels/${conversation.id}`);
  }
</script>

<div class="app-canvas min-h-screen pb-10">
  <!-- Hero, "Etkinlik Hakkında" card, and the message button all share this
       single max-w-sm column so every component ends up the same width. -->
  <main class="px-5 pt-6 max-w-sm mx-auto space-y-4">
    <!-- Top Hero Banner Image (Mockups 8 & 10) -->
    <div class="relative w-full aspect-[4/3.8] rounded-[2.5rem] overflow-hidden shadow-md">
      <img src={event.image} alt={event.title} class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/25 to-black/30"></div>

      <!-- Floating Top Action Buttons -->
      <div class="absolute top-5 left-5 right-5 flex items-center justify-between z-10">
        <a
          href="/discover"
          aria-label={t('eventDetail.back')}
          class="w-10 h-10 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center text-foreground shadow-sm hover:bg-white transition-colors"
        >
          <ArrowLeft class="w-4 h-4 text-[#ef4444]" />
        </a>

        <div class="flex items-center gap-2.5">
          <button
            type="button"
            aria-label={t('eventDetail.share')}
            class="w-10 h-10 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center text-[#ef4444] shadow-sm hover:bg-white transition-colors cursor-pointer"
          >
            <Share2 class="w-4 h-4" />
          </button>
          <button
            type="button"
            aria-label={t('common.favorite')}
            class="w-10 h-10 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center text-[#ef4444] shadow-sm hover:bg-white transition-colors cursor-pointer"
            onclick={() => (favorited = !favorited)}
          >
            <Heart class="w-4 h-4 {favorited ? 'fill-current' : ''}" />
          </button>
        </div>
      </div>

      <!-- Title Overlay at bottom of hero -->
      <div class="absolute bottom-5 left-5 right-5 z-10">
        <div class="space-y-1 text-white">
          <h1 class="text-2xl font-black tracking-tight drop-shadow-sm">{event.title}</h1>
          <div class="flex items-center gap-1.5 text-xs text-white/90">
            <MapPin class="w-3.5 h-3.5 text-white/80" />
            <span>{event.venue}</span>
          </div>
          <div class="flex items-center gap-1.5 text-xs text-white/80">
            <Calendar class="w-3.5 h-3.5 text-white/80" />
            <span>{event.date} • {event.time}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Etkinlik Hakkında Card -->
    <div class="rounded-3xl bg-white dark:bg-card border border-border/80 p-5 shadow-xs space-y-4">
      <h2 class="text-lg font-bold text-foreground">{t('eventDetail.about')}</h2>
      <p class="text-xs text-muted-foreground leading-relaxed">
        {event.description}
      </p>
    </div>

    <button
      type="button"
      onclick={messageOrganizer}
      class="w-full h-12 rounded-2xl bg-white dark:bg-card border border-border/80 text-foreground font-semibold text-sm flex items-center justify-center gap-2 shadow-xs hover:border-[#ea580c]/30 active:scale-[0.99] transition-all cursor-pointer"
    >
      <MessageCircle class="w-4 h-4 text-[#ea580c]" />
      <span>{t('eventDetail.message_organizer')}</span>
    </button>
  </main>
</div>
