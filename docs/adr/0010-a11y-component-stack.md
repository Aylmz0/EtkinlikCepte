# ADR-0010: Erişilebilirlik ve bileşen katmanları

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §3.1

## Karar

Üç katman: **bits-ui** (davranış, npm'den), **shadcn-svelte** (görünüm, kopyalanan kod), **bizim yazdıklarımız** (alan parçaları, `packages/ui/src/lib/features/`).

## Gerekçe

**bits-ui.** Bağımsız bileşen kütüphaneleri React'e bağlı: Radix UI React için, Headless UI React için, MUI React için. Svelte tarafında ölçülebilir seçenek bits-ui (haftalık 1,37M indirme). Erişilebilir bileşenler için Svelte tarafında başka bir yol yok.

**shadcn-svelte kopyalanır, kurulmaz.** Görünüm kodları `packages/ui/src/lib/components/ui/` altına kopyalanır ve ekip tarafından düzenlenebilir. Bağımlılık olarak kurulsaydı görünüm değiştirilemezdi.

**Alan parçaları ayrı.** `EventCard`, `QRDisplay`, `PostCard` gibi parçalar birden çok ekranda kullanılır. `ui/` altında değil `features/` altında dururlar — çünkü bunlar bize ait iş kurallarını da taşır.

## Sonuçlar

**Sınır kuralı:** `packages/ui` içinde sunucu isteği, jeton veya rota bilgisi olmaz. `routes/` içinde elle yazılmış stil sınıfı olmaz.

**Bu ayrım sayesinde** tasarım değişince erişilebilirlik bozulmaz, davranış değişince tasarım bozulmaz. shadcn-svelte güncellenirse `ui/` altındaki kopyalar değişmez; davranış bits-ui'nin işidir.

**13 alan parçası Sprint 1'de çıkar:**

| Alan | Parçalar |
|---|---|
| Keşif | `EventCard`, `VenueMarker`, `FilterSheet` |
| Bilet | `TicketRow`, `QRDisplay` |
| Kulüp | `ClubBadge`, `PostCard`, `PostComposer`, `FollowButton` |
| Sohbet | `ChatBubble`, `PresenceDot`, `VoiceBar`, `VideoTile` |