# ADR-0006: Tahsilat yapılmaz

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §4.2

## Karar

Uygulama üzerinden ödeme alınmaz. Bilet akışı tam çalışır; ödeme onayını organizatör elle verir.

## Gerekçe

Tahsilat için ödeme kuruluşuyla (iyzico, PayTR, Stripe) sözleşme, vergi numarası, banka onayı ve KVKK kapsamında ek sözleşmeler gerekir. Bu hukuki bir engeldir, teknik değil — çözümü yoktur, süresi belirsizdir.

Bilet akışının tamamı yine de kurulur. `reserved → pending_payment → paid → used` durum makinesi, 15 dakikalık rezervasyon, QR üretimi ve kapıda okutma çalışır. Tek eksik olan ödeme kuruluşuna API çağrısıdır; o kısmı organizatör tek dokunuşla yerine getirir.

## Sonuçlar

**Kullanıcı tarafında bekleme var.** `pending_payment` durumunda kullanıcı birkaç saniye bekler, sonra QR geçerli olur. Bu akış demo anında izlenebilir.

**Organizatöre yeni bir ekran yükü.** Kulüp panelinde `pending_payment` listesi ve onay düğmesi var. Bu ekran P2'nin işi.

**Toplanan etkinlikler zaten yönlendirme yapıyor.** Kaynak siteden gelen etkinlikte "Bilet al" düğmesi o sitenin satış sayfasını açar. Bu, kapsam kararıyla tutarlı: uygulama hiçbir koşulda para almaz.

**İleride açılabilir.** Ödeme eklenirse durum makinesinde `pending_payment` → `paid` geçişi otomatikleşir, şema değişmez.