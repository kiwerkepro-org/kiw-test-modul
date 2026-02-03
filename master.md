# KI-WERKE MASTER SOURCE OF TRUTH
**Status:** v1.1.0 (Hardened & Lean - 03.02.2026)
**Zweck:** Zentrale Verbindlichkeit für Marke, Design, Code und Architektur.

## 0. GLOBAL SECURITY GATEKEEPER (SYSTEM-AGNOSTIC)
- **Isolation-First:** Nur Antigravity hat Schreibrechte auf Projekte im `developing` Verzeichnis. Andere IDEs oder Tools sind für Code-Änderungen untersagt.
- **Integritäts-Check:** Jeder externe Code (Snippets, Bibliotheken) muss vor der Integration vom Agenten in einer isolierten Umgebung auf versteckte Manipulation, Backdoors oder unsichere Funktionen geprüft werden.
- **Zero-Trust-Vorschläge:** Der Agent lehnt Code-Vorschläge ab, die Sicherheitsstandards verletzen (z.B. unsichere Datenübergabe), selbst wenn diese explizit angefordert werden, und bietet stattdessen die gehärtete Alternative an.
- **Audit-Pflicht:** Jede sicherheitsrelevante Änderung (Dateizugriff, API-Keys, GitHub-Push) erfordert eine kurze schriftliche Begründung des Agenten und die Freigabe durch den "Human-in-the-Loop".

## 1. MARKENKERN & TONALITÄT
- **Markenname:** KI-WERKE (Immer Versalien).
- **Tonalität:** Klar, direkt, technisch fundiert, Werkstatt-Charakter.

## 2. DESIGN SYSTEM (BENTO GRID @ SUPABASE)
- **Stil:** Bento Grid @ Supabase (Klare Kanten, hohe Informationsdichte).
- **Farben:**
    - **Hintergrund:** `#0A0F1A` (Deep Navy)
    - **Panels:** `#111827` (Panel Grey)
    - **Accent:** `#00E0B8` (Cyan Neon)
    - **Text:** `#F4F5F7` (Off-White)
- **Framework:** Tailwind CSS (JIT-Mode).
- **Icons:** Lucide-Icons (Color: `#00E0B8`). Legacy Dashicons sind untersagt.

## 3. ARCHITEKTUR & STRUKTUR
- **Namespaces:** PSR-4 konform `KIW\Module\Slug\...`.
- **Dateistruktur:** `src/` Ordner für Logik; strikte Trennung von Assets.
- **Smart Loading:** Admin-Scripte/Logik dürfen NIEMALS im Frontend geladen werden.
- **Discovery:** Module werden ausschließlich über die `module.json` (Schema v1) erkannt.

## 4. SECURITY & DATA HANDLING (WP-HARDENED)
- **Sanitization:** KEINE direkten Superglobals (`$_POST`, `$_GET`). Nutzung von `filter_input()` oder WP-Sanitization.
- **Database:** KEINE direkten SQL-Queries. Ausschließlich `$wpdb->prepare()`.
- **AJAX Security:** Jeder Handler MUSS `check_ajax_referer()` und `current_user_can()` enthalten.
- **Visibility:** Domain-Lock Prüfung gegen `domain_lock` Feld in `module.json`.

## 5. PERFORMANCE & RESOURCE MANAGEMENT (LEAN STANDARD)
- **Lean by Design:** Nutze native WP-APIs. Vermeide unnötige Overheads.
- **Caching:** Nutze Transients (`set_transient`) für teure Operationen.
- **Resource Declaration:** Module mit hohem Ressourcenbedarf (z.B. Sync-Engines) müssen dies im Header explizit deklarieren.

## 6. SYSTEM-HYGIENE & CORE PROTECTION
- **Anti-Ghosting:** Force `wp_cache_flush()` und `clearstatcache()` nach Modul-Aktionen.
- **Update-Rescue:** "In-Place-Overwrite" für `kiw-suite` (Windows-Lock-Prävention).
- **Error Handling:** Keine Silent Fails. Nutzung von `WP_Error` für UI-Feedback.

## 7. WORKFLOW & AUDIT
- **Source Control:** Alle Änderungen über die `kiwerkepro-org` Organisation.
- **Logging:** Alle Sync-Aktionen im Master-Sync-Sheet (Tab 2) protokollieren.
- **Human-in-the-Loop:** Agenten agieren als Partner; Bestätigung bei destruktiven Aktionen einholen.