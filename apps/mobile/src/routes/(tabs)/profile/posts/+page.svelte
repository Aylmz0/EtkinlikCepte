<!--
  @component ProfilePostsPage
  @desc The signed-in user's own previously shared club posts (distinct from
    the public /feed, which lists everyone's posts) (§1.6, Owner: P6).
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, Heart } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  const myPosts = [
    {
      id: 1,
      club: 'Rakometno Igralishte',
      text: 'Bu akşamki maç için kapılar 19:00’da açılıyor, görüşmek üzere!',
      date: '3 gün önce',
      likes: 24,
      image:
        'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=400&q=80',
    },
    {
      id: 2,
      club: 'MKC Kültür Merkezi',
      text: 'Yeni sergi için biletler bugün açıldı.',
      date: '1 hafta önce',
      likes: 11,
      image: null,
    },
  ];
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto space-y-5 pb-12">
  <div class="flex items-center gap-3 pt-2">
    <a
      href="/profile"
      aria-label={t('common.back')}
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('profilePosts.title')}</h1>
  </div>

  {#if myPosts.length === 0}
    <p class="text-sm text-muted-foreground text-center py-10">{t('profilePosts.empty')}</p>
  {/if}

  <div class="space-y-3.5">
    {#each myPosts as post (post.id)}
      <div
        class="rounded-3xl bg-white dark:bg-card border border-border/80 p-4 shadow-xs space-y-3"
      >
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-foreground">{post.club}</span>
          <span class="text-[11px] text-muted-foreground">{post.date}</span>
        </div>
        <p class="text-xs text-muted-foreground leading-relaxed">{post.text}</p>
        {#if post.image}
          <img src={post.image} alt="" class="w-full h-36 rounded-2xl object-cover" />
        {/if}
        <div
          class="flex items-center gap-1.5 text-xs text-[#ef4444] pt-1 border-t border-border/60"
        >
          <Heart class="w-3.5 h-3.5 fill-current" />
          <span>{post.likes}</span>
        </div>
      </div>
    {/each}
  </div>
</div>
