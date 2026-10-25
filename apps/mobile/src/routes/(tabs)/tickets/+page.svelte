<!--
  @component SavedTicketsPage
  @desc Saved events and offline tickets screen matching the design system.
  Props: None
  Events: None
-->
<script lang="ts">
  import { Heart, QrCode, Calendar, MapPin, ArrowUpRight } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  // Frontend-only state: unfavoriting removes the card from this saved list.
  let savedItems = $state([
    {
      id: 'galija-bitola',
      title: 'Galija - Bitola',
      date: '17 TEM • 18:00',
      venue: 'Rakometno Igralishte',
      image:
        'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=400&q=80',
      hasTicket: true,
    },
    {
      id: 'taksirat',
      title: 'Taksirat Festival',
      date: '6 ARA • 19:30',
      venue: 'Boris Trajkovski Arena',
      image:
        'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=400&q=80',
      hasTicket: false,
    },
  ]);

  function removeFromSaved(id: string) {
    savedItems = savedItems.filter((item) => item.id !== id);
  }
</script>

<div class="px-5 py-4 space-y-5 max-w-sm mx-auto">
  <!-- Title -->
  <div class="space-y-1 pt-1">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">
      {t('savedTickets.title')}
    </h1>
    <p class="text-xs text-muted-foreground">{t('savedTickets.subtitle')}</p>
  </div>

  <!-- Saved Items List -->
  {#if savedItems.length === 0}
    <p class="text-sm text-muted-foreground text-center py-10">{t('savedTickets.empty')}</p>
  {/if}
  <div class="space-y-3.5">
    {#each savedItems as item (item.id)}
      <div
        class="rounded-3xl bg-white dark:bg-card border border-border/80 p-4 shadow-xs space-y-3"
      >
        <div class="flex items-center gap-3.5">
          <img
            src={item.image}
            alt={item.title}
            class="w-16 h-16 rounded-2xl object-cover shrink-0"
          />
          <div class="space-y-1 flex-1">
            <h2 class="text-sm font-bold text-foreground leading-tight">
              {item.title}
            </h2>
            <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Calendar class="w-3 h-3 text-[#ef4444]" />
              <span>{item.date}</span>
            </div>
            <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
              <MapPin class="w-3 h-3 text-[#ea580c]" />
              <span>{item.venue}</span>
            </div>
          </div>

          <button
            type="button"
            aria-label={t('savedTickets.remove')}
            class="p-2 text-[#ef4444] hover:opacity-80 transition-opacity cursor-pointer self-start"
            onclick={() => removeFromSaved(item.id)}
          >
            <Heart class="w-4 h-4 fill-current" />
          </button>
        </div>

        <div class="pt-2 border-t border-border/60 flex items-center justify-end">
          {#if item.hasTicket}
            <div
              class="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 text-xs font-semibold"
            >
              <QrCode class="w-3.5 h-3.5" />
              <span>{t('savedTickets.ticket_ready')}</span>
            </div>
          {:else}
            <a
              href="/events/{item.id}"
              class="inline-flex items-center gap-1 text-xs font-semibold text-[#ef4444] hover:underline"
            >
              <span>{t('savedTickets.details')}</span>
              <ArrowUpRight class="w-3 h-3" />
            </a>
          {/if}
        </div>
      </div>
    {/each}
  </div>
</div>
