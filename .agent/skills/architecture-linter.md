---
description: Eiserne Architektur-Regeln für KI-WERKE Plugins & Themes
---

# Architecture Linter Skill (v1.1.0)

Du bist darauf programmiert, jegliche Code-Erstellung zu blockieren, die gegen folgende Kern-Prinzipien verstößt:

## 1. Zero-CDN Policy (Lokalitäts-Gebot)
- **Verbot:** Keine Einbindung externer Assets via URL (z.B. https://cdn..., https://unpkg..., Google Fonts).
- **Pflicht:** Alle Bibliotheken (JS, CSS, Fonts) müssen im lokalen `assets/` Ordner liegen.
- **Aktion:** Melde einen Fehler, wenn eine externe Asset-URL im Code gefunden wird.

## 2. Output Security (Escaping-Zwang)
- **Verbot:** Kein `echo $variable` ohne Absicherung.
- **Pflicht:** Nutze zwingend `esc_html()`, `esc_attr()`, `esc_url()` oder `wp_kses()` bei jeder Ausgabe.
- **Ausnahme:** Nur wenn die Variable unmittelbar vorher durch eine sichere WP-Funktion generiert wurde.

## 3. Input Integrity (Sanitization-Zwang)
- **Verbot:** Direkter Zugriff auf `$_POST`, `$_GET`, `$_REQUEST` ohne Bereinigung.
- **Pflicht:** Nutze `sanitize_text_field()`, `absint()` oder ähnliche Funktionen sofort beim Einlesen.

## 4. State Protection (Nonce-Pflicht)
- **Pflicht:** Jede AJAX-Anfrage und jedes Formular MUSS eine Nonce-Prüfung (`check_admin_referer` oder `wp_verify_nonce`) enthalten.

## 5. UI-Standard (Bento & Soft UI)
- **Pflicht:** Admin-Oberflächen müssen dem Bento Box Grid System folgen.
- **Farben:** Nutze strikt WP-Blue (#2271b1) und Premium-Gold (#D4AF37).

**Anweisung:** Wenn eine dieser Regeln verletzt wird, unterbrich den Prozess und fordere Korrektur, bevor der Code finalisiert wird.