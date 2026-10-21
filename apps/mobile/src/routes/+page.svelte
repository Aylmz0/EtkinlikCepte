<!--
  @component HomePage
  @desc Root landing and quick launch hub for the mobile shell.
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
  import { Sparkles, ArrowRight, User, Settings } from '@lucide/svelte';
</script>

<main class="flex flex-col min-h-screen px-6 py-8 max-w-sm mx-auto justify-between">
  <!-- Brand Header -->
  <header class="pt-6 space-y-3">
    <div
      class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-[#fef2e8] text-[#ea580c] border border-[#fed7aa]/50"
    >
      <Sparkles class="w-3.5 h-3.5" />
      <span>EtkinlikCepte v0.1.0</span>
    </div>

    <h1 class="text-4xl font-black tracking-tight text-foreground">
      keşfet<span class="text-primary">.</span>
    </h1>
    <p class="text-sm text-muted-foreground leading-relaxed">
      {t('app.tagline')}
    </p>
  </header>

  <!-- P6 Quick Action Cards -->
  <section class="space-y-4 my-auto py-6">
    <a
      href="/discover"
      class="group flex items-center justify-between p-4 rounded-2xl border border-border/80 bg-white dark:bg-card shadow-xs hover:border-primary/50 hover:shadow-sm transition-all"
    >
      <div class="space-y-0.5">
        <span class="text-base font-bold text-foreground">Uygulamaya Gir (Keşfet)</span>
        <p class="text-xs text-muted-foreground">Etkinlikler ve Mekanlar</p>
      </div>
      <div
        class="w-9 h-9 rounded-full bg-[#fef2e8] text-[#ea580c] flex items-center justify-center group-hover:translate-x-0.5 transition-transform"
      >
        <ArrowRight class="w-4 h-4" />
      </div>
    </a>

    <div class="grid grid-cols-2 gap-3 pt-1">
      <a
        href="/profile"
        class="flex flex-col p-4 rounded-2xl border border-border/80 bg-white dark:bg-card shadow-xs hover:border-primary/40 transition-colors"
      >
        <div
          class="w-8 h-8 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 flex items-center justify-center mb-2"
        >
          <User class="w-4 h-4" />
        </div>
        <span class="text-sm font-bold text-foreground">Profilim</span>
        <span class="text-xs text-muted-foreground">Kullanıcı Ekranı</span>
      </a>

      <a
        href="/settings"
        class="flex flex-col p-4 rounded-2xl border border-border/80 bg-white dark:bg-card shadow-xs hover:border-primary/40 transition-colors"
      >
        <div
          class="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 flex items-center justify-center mb-2"
        >
          <Settings class="w-4 h-4" />
        </div>
        <span class="text-sm font-bold text-foreground">Ayarlar</span>
        <span class="text-xs text-muted-foreground">Sistem & Tercihler</span>
      </a>
    </div>

    <div class="pt-3 flex gap-3">
      <a
        href="/login"
        class="flex-1 h-12 rounded-2xl bg-primary text-primary-foreground font-semibold text-sm flex items-center justify-center shadow-xs hover:bg-[#dc2626] transition-colors"
      >
        {t('auth.login')}
      </a>
      <a
        href="/register"
        class="flex-1 h-12 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground font-semibold text-sm flex items-center justify-center shadow-xs hover:bg-muted/40 transition-colors"
      >
        {t('auth.register')}
      </a>
    </div>
  </section>

  <!-- Footer -->
  <footer class="py-4 text-center text-xs text-muted-foreground/60">
    <span>P6 (Abdullah Hilal) • Core & Design System</span>
  </footer>
</main>
