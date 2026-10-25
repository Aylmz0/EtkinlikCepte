<!--
  @component AboutPage
  @desc Application details and open data attributions (§1.6, §4.3, Owner: P7).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
  import { ArrowLeft, MapPin, Code2 } from '@lucide/svelte';
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto space-y-5 pb-12">
  <div class="flex items-center gap-3 pt-2">
    <a
      href="/settings"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('about.title')}</h1>
  </div>

  <div
    class="rounded-3xl bg-white dark:bg-card border border-border/80 p-5 shadow-xs space-y-2 text-center"
  >
    <span class="text-2xl font-black text-[#ea580c] tracking-tight">Keşfet.</span>
    <p class="text-xs text-muted-foreground">{t('app.tagline')}</p>
    <p class="text-[11px] text-muted-foreground/70">{t('app.name')} • v0.1.0</p>
  </div>

  <div class="rounded-3xl bg-white dark:bg-card border border-border/80 p-5 shadow-xs space-y-3">
    <div class="flex items-center gap-2 text-foreground">
      <MapPin class="w-4 h-4 text-[#ea580c]" />
      <h2 class="text-sm font-bold">{t('about.attribution_title')}</h2>
    </div>
    <p class="text-xs text-muted-foreground leading-relaxed">
      {t('about.attribution_body')}
    </p>
  </div>

  <div class="rounded-3xl bg-white dark:bg-card border border-border/80 p-5 shadow-xs space-y-3">
    <div class="flex items-center gap-2 text-foreground">
      <Code2 class="w-4 h-4 text-muted-foreground" />
      <h2 class="text-sm font-bold">{t('about.open_source_title')}</h2>
    </div>
    <p class="text-xs text-muted-foreground leading-relaxed">
      {t('about.open_source_body')}
    </p>
  </div>
</div>
