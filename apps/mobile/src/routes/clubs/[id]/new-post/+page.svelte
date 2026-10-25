<!--
  @component ClubNewPostPage
  @desc Club post creator with photo upload support (§1.6, §4.13, Owner: P2).
    Publishing requires the backend upload/post endpoint and is not wired
    here — the composer accepts local text input but submit stays inert.
    Photos allowed, max 4, no video upload (§4.13).
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, ImagePlus } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  let draft = $state('');
  const photoSlots = [0, 1, 2, 3];
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto space-y-5 pb-12">
  <div class="flex items-center gap-3 pt-2">
    <a
      href="../"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('newPost.title')}</h1>
  </div>

  <div class="rounded-3xl bg-white dark:bg-card border border-border/80 p-4 shadow-xs space-y-4">
    <textarea
      bind:value={draft}
      rows="4"
      placeholder={t('newPost.placeholder')}
      class="w-full px-3.5 py-3 rounded-2xl border border-border/80 bg-background text-sm placeholder:text-muted-foreground/60 shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-all resize-none"
    ></textarea>

    <div class="grid grid-cols-4 gap-2">
      {#each photoSlots as slot (slot)}
        <div
          class="aspect-square rounded-xl border border-dashed border-border/80 flex items-center justify-center text-muted-foreground/60"
        >
          <ImagePlus class="w-4 h-4" />
        </div>
      {/each}
    </div>
    <p class="text-[11px] text-muted-foreground/70">
      {t('newPost.photo_hint')}
    </p>
  </div>

  <button
    type="button"
    disabled
    class="w-full h-12 rounded-2xl bg-primary/40 text-primary-foreground font-semibold text-sm shadow-xs cursor-not-allowed"
  >
    {t('newPost.submit')}
  </button>
</div>
