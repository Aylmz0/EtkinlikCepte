<!--
  @component SettingsPage
  @desc Settings screen matching UI mockup Image 5 (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import {
    User,
    Lock,
    Bell,
    MessageSquare,
    Sun,
    Languages,
    Smartphone,
    Shield,
    Info,
    UserX,
    LogOut,
    ChevronRight,
    ArrowLeft,
  } from '@lucide/svelte';
</script>

<div class="min-h-screen px-5 py-6 max-w-sm mx-auto space-y-5 pb-12">
  <!-- Top Navigation & Title -->
  <div class="flex items-center gap-3 pt-2">
    <a
      href="/(tabs)/profile"
      aria-label="Geri"
      class="w-9 h-9 rounded-full bg-white dark:bg-card border border-border/80 flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
    </a>
    <h1 class="text-2xl font-bold tracking-tight text-foreground">Ayarlar</h1>
  </div>

  <!-- Group 1: Profile & Security -->
  <section
    class="rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs divide-y divide-border/60 overflow-hidden"
  >
    <a
      href="/(tabs)/profile"
      class="flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <User class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Profil Bilgileri</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <button
      type="button"
      class="w-full flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors text-left cursor-pointer"
    >
      <div class="flex items-center gap-3">
        <Lock class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Şifre Değiştir</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </button>
  </section>

  <!-- Group 2: App & Preferences -->
  <section
    class="rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs divide-y divide-border/60 overflow-hidden"
  >
    <a
      href="/notifications"
      class="flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <Bell class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Bildirimler</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <a
      href="/(tabs)/messages"
      class="flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <MessageSquare class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Sohbetler</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <button
      type="button"
      class="w-full flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors text-left cursor-pointer"
    >
      <div class="flex items-center gap-3">
        <Sun class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Görünüm</span>
      </div>
      <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
        <span>Açık</span>
        <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
      </div>
    </button>

    <button
      type="button"
      class="w-full flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors text-left cursor-pointer"
    >
      <div class="flex items-center gap-3">
        <Languages class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Uygulama Dili</span>
      </div>
      <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
        <span>Türkçe</span>
        <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
      </div>
    </button>

    <button
      type="button"
      class="w-full flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors text-left cursor-pointer"
    >
      <div class="flex items-center gap-3">
        <Smartphone class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Cihaz İzinleri</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </button>
  </section>

  <!-- Group 3: Privacy & About -->
  <section
    class="rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs divide-y divide-border/60 overflow-hidden"
  >
    <button
      type="button"
      class="w-full flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors text-left cursor-pointer"
    >
      <div class="flex items-center gap-3">
        <Shield class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Gizlilik</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </button>

    <a
      href="/about"
      class="flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors"
    >
      <div class="flex items-center gap-3">
        <Info class="w-4 h-4 text-muted-foreground" />
        <span class="text-sm font-medium text-foreground">Hakkında</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </a>

    <button
      type="button"
      class="w-full flex items-center justify-between px-4 py-3.5 hover:bg-muted/40 transition-colors text-left cursor-pointer"
    >
      <div class="flex items-center gap-3 text-destructive">
        <UserX class="w-4 h-4" />
        <span class="text-sm font-medium">Hesabı Kapat</span>
      </div>
      <ChevronRight class="w-4 h-4 text-muted-foreground/60" />
    </button>
  </section>

  <!-- Bottom Log Out Button -->
  <div class="pt-2">
    <button
      type="button"
      class="w-full h-13 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-xs flex items-center justify-center gap-2 text-destructive font-semibold text-sm hover:bg-destructive/5 active:scale-[0.99] transition-all cursor-pointer"
    >
      <LogOut class="w-4 h-4" />
      <span>Çıkış Yap</span>
    </button>
  </div>
</div>
