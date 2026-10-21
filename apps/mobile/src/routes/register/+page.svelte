<!--
  @component RegisterPage
  @desc Authentication register screen matching UI mockup Image 4 (§1.6, Owner: P6 Abdullah Hilal).
  Props: None
  Events: None
-->
<script lang="ts">
  import { t } from '$lib/i18n.js';
</script>

<div class="flex flex-col min-h-screen px-6 py-10 max-w-sm mx-auto justify-between">
  <!-- Top section / form -->
  <div class="pt-6 space-y-6">
    <h1 class="text-3xl font-extrabold tracking-tight text-foreground">Aramıza Katılın</h1>

    <form class="space-y-4" onsubmit={(e) => e.preventDefault()}>
      <div class="space-y-1.5">
        <label for="fullName" class="text-xs font-medium text-foreground/80">Ad Soyad</label>
        <input
          id="fullName"
          type="text"
          placeholder="Adınızı ve soyadınızı girin"
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>

      <div class="space-y-1.5">
        <label for="email" class="text-xs font-medium text-foreground/80">E-posta</label>
        <input
          id="email"
          type="email"
          placeholder="E-posta adresinizi girin"
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>

      <div class="space-y-1.5">
        <label for="password" class="text-xs font-medium text-foreground/80">Şifre</label>
        <input
          id="password"
          type="password"
          placeholder="Şifrenizi girin"
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>

      <div class="space-y-1.5">
        <label for="passwordConfirm" class="text-xs font-medium text-foreground/80"
          >Şifre Tekrarı</label
        >
        <input
          id="passwordConfirm"
          type="password"
          placeholder="Şifrenizi tekrar girin"
          class="w-full h-12 px-4 rounded-2xl border border-border/80 bg-white dark:bg-card text-foreground placeholder:text-muted-foreground/60 text-sm shadow-xs focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
        />
      </div>

      <div class="pt-4">
        <button
          type="submit"
          class="w-full h-13 rounded-2xl bg-primary text-primary-foreground font-semibold text-base shadow-sm hover:bg-[#dc2626] active:scale-[0.99] transition-all cursor-pointer"
        >
          {t('auth.register')}
        </button>
      </div>
    </form>
  </div>

  <footer class="py-6 text-center text-xs text-muted-foreground">
    <span>Zaten hesabınız var mı?</span>
    <a href="/login" class="font-semibold text-primary hover:underline ml-1">
      {t('auth.login')}
    </a>
  </footer>
</div>
