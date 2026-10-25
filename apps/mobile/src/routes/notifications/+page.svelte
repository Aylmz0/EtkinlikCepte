<!--
  @component NotificationsPage
  @desc In-app notification center (§1.6, §4.8, Owner: P5).
  Props: None
  Events: None
-->
<script lang="ts">
  import { ArrowLeft, Ticket, Heart, Users, MessageSquare } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  const notifications = [
    {
      id: 1,
      icon: Ticket,
      color: 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/40',
      title: 'Biletiniz hazır',
      detail: 'Galija - Bitola biletiniz cüzdanınıza eklendi.',
      time: '2 sa önce',
    },
    {
      id: 2,
      icon: Heart,
      color: 'text-[#ef4444] bg-[#fef2f2] dark:bg-[#3a1b1b]',
      title: 'Etkinlik hatırlatması',
      detail: 'Taksirat Festival yarın başlıyor.',
      time: '5 sa önce',
    },
    {
      id: 3,
      icon: Users,
      color: 'text-[#ea580c] bg-[#fef2e8] dark:bg-[#2a221b]',
      title: 'Yeni takipçi',
      detail: 'Bir kullanıcı kulübünüzü takip etmeye başladı.',
      time: '1 gün önce',
    },
    {
      id: 4,
      icon: MessageSquare,
      color: 'text-[#00c4b4] bg-[#e6faf8] dark:bg-[#102a28]',
      title: 'Yeni mesaj',
      detail: 'Sohbetlerinizde okunmamış bir mesaj var.',
      time: '2 gün önce',
    },
  ];
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
    <h1 class="text-2xl font-bold tracking-tight text-foreground">{t('notifications.title')}</h1>
  </div>

  <div class="space-y-3">
    {#each notifications as item (item.id)}
      {@const Icon = item.icon}
      <div
        class="flex items-start gap-3 p-3.5 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs"
      >
        <div class="w-9 h-9 rounded-full flex items-center justify-center shrink-0 {item.color}">
          <Icon class="w-4 h-4" />
        </div>
        <div class="flex-1 space-y-0.5">
          <h2 class="text-sm font-bold text-foreground leading-snug">{item.title}</h2>
          <p class="text-xs text-muted-foreground leading-relaxed">{item.detail}</p>
        </div>
        <span class="text-[11px] text-muted-foreground/70 shrink-0 pt-0.5">{item.time}</span>
      </div>
    {/each}
  </div>
</div>
