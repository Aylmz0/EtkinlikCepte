# ADR-0007: CSS çerçevesi — Tailwind CSS 4

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §3.1, §3.5

## Karar

Tailwind CSS 4, `@tailwindcss/vite` eklentisiyle. UnoCSS kullanılmaz.

## Gerekçe

| Ölçüt | Tailwind v4 | UnoCSS |
|---|---|---|
| Haftalık npm indirmesi | 163.032.225 | 960.371 |
| Svelte desteği | Resmî | Var |
| VS Code IntelliSense | Resmî eklenti | Yok |
| shadcn-svelte uyumu | Doğrudan | Uyarlama gerekir |

Yaklaşık **170 kat** indirme farkı, iki tarafın da aynı işi yaptığını gösteriyor. Bu, bakım ve topluluk büyüklüğünün en ucuz ölçütü: bir sorun çıktığında cevap bulma ihtimali.

shadcn-svelte, bileşenlerini Tailwind sınıflarıyla dağıtıyor. Başka bir çerçeveyle kullanmak, her bileşen için sınıf eşleme tablosu demek — yedi kişilik ekip için sürdürülemez.

## Tailwind v4 + IntelliSense

Tailwind v4 CSS-first konfigürasyona geçti: `tailwind.config.ts` yerine `@theme` bloğu kullanılıyor. Bu, resmî VS Code eklentisini bozuyor (tailwindcss/tailwindcss#15132, tailwindcss/tailwindcss-intellisense#1170).

**Çözüm:** Minimal bir `tailwind.config.ts` tutulur. İçeriği sadece IntelliSense için gereken kaynak taraması ayarlarıdır, tema tanımı değil. Gerçek tema `packages/ui/src/tokens.css` içindeki `@theme` bloğunda durur.

Sprint 0 çıkış ölçütü: IntelliSense'in sınıf önerisi verdiği doğrulanır (0.4).

## Sonuçlar

**İki yer değil, tek yer.** Tema kaynağı `tokens.css`'tir. `tailwind.config.ts` yalnızca editör içindir ve CI'da çalışma zamanında kullanılmaz — iki dosya çelişirse `tokens.css` kazanır.

**Bu maliyet kabul edildi.** Ekip, IntelliSense olmayan Tailwind v4 kurulumuna göre bir dosya fazla yaşıyor. Yazarken yanlış sınıf adı yazıp nedenini aramaktan ucuz.