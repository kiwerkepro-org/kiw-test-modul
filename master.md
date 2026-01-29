# Serenity WP Design System (Master)

## 🎯 Zielsetzung
Dieses Plugin soll eine Brücke schlagen zwischen der nativen WordPress-Admin-Erfahrung und modernem High-End-Design.

## 🏗️ Architektur-Regeln
- **Backend (Admin):** - Nutze die WordPress-Core-Farbpalette für die Integration.
    - Optimiere die UX durch "Bento Box" Layouts für Einstellungen.
    - Vermeide veraltete WP-Tabellen-Layouts; nutze moderne Flexbox/Grid-Container.
- **Frontend (User):**
    - Standard-Stil: **Soft UI Evolution** (Subtile Schatten, organische Formen).
    - Performance-First: Nutze Tailwind CSS (JIT mode).

## 🎨 Farb-Logik (WordPress Hybrid)
- **WP-Blue:** #2271b1 (Für primäre Aktionen im Backend)
- **Success:** #46b450
- **Warning:** #ffb900
- **Surface-Light:** #f0f0f1 (WP Background)
- **Premium-Accent:** #D4AF37 (Gold für Luxus-Features/Upsells)

## ✍️ Typografie
- **Admin:** System-Fonts (Inter, Segoe UI, Roboto).
- **Frontend:** Cormorant Garamond (Headings) / Montserrat (Body).

## 🚫 Anti-Patterns (Nicht erlaubt!)
- Keine Emojis als Icons -> Immer Lucide/Heroicons (SVG) verwendet.
- Keine harten 1px Rahmen -> Nutze `ring-1` oder subtile Schatten.
- Keine überladenen Menüs -> Nutze progressive Disclosure (einklappbare Sektionen).

## 🛠️ Pre-Delivery Check für WordPress
- [ ] Alle UI-Elemente sind übersetzbar (`__()` oder `_e()`).
- [ ] Responsive Breakpoints: 375px, 768px, 1024px, 1440px.
- [ ] Hover-States haben `transition-duration: 200ms`.
- [ ] Kontrastverhältnis erfüllt WCAG AA.