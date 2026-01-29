# Task: Restrukturierung Template nach KIW-Direktive

Dieses Dokument beschreibt die Schritte zur Restrukturierung des Repositories gemäß der KIW-Direktive (Bento Box / Soft UI Standard).

## 📋 Analyse & Status Quo
- **Aktuelle Struktur:**
  - `plugin/` enthält `kiw-internal-tools.php`, `blueprint-module.php` und `admin-dashboard.php`.
  - Root enthält eine veraltete `blueprint-module.php`.
  - `/design-system/` enthält Architektur-Dokumente.
- **Zielstruktur:**
  - Alle PHP-Kern-Dateien im Root.
  - Dedizierte Ordner: `/assets/css`, `/assets/js`, `/includes`, `/views`.
  - Metadaten-Zentralisierung in `kiw/module.json`.
  - Platzhalter für Name/Slug (`{{MODULE_NAME}}`, `{{MODULE_SLUG}}`).

---

## 🛠️ Phasen-Plan

### Phase 1: Vorbereitung & Verzeichnisstruktur
- [ ] Erstellen der Ordner im Root:
  - `assets/css`
  - `assets/js`
  - `includes`
  - `views`
- [ ] Erstellen des Ordners `kiw` für Metadaten.

### Phase 2: Datei-Migration (Rooting)
- [ ] **Blueprint:** Kopiere `plugin/blueprint-module.php` (1.5 KB) nach Root und überschreibe die dortige Version.
- [ ] **Hauptdatei:** Kopiere `plugin/kiw-internal-tools.php` nach Root (da dies der Host der Metadaten ist).
- [ ] **Views:** Verschiebe `plugin/admin-dashboard.php` nach `/views/admin-dashboard.php`.
- [ ] **Design:** Verschiebe `design-system/master.md` direkt in das Root-Verzeichnis.

### Phase 3: Metadaten & Platzhalter
- [ ] Erstelle `kiw/module.json` (Schema V1) mit folgendem Inhalt (Platzhalter-zentriert):
  ```json
  {
    "schema": 1,
    "name": "{{MODULE_NAME}}",
    "slug": "{{MODULE_SLUG}}",
    "version": "1.0.0",
    "type": "module",
    "entry": "blueprint-module.php"
  }
  ```
- [ ] Aktualisiere die Plugin-Header in der Hauptdatei (jetzt im Root) mit den Platzhaltern für Name und Text-Domain.

### Phase 4: Pfadanpassungen & Logik-Fixes
- [ ] In der Hauptdatei (jetzt im Root):
  - Passe den Pfad zur View an (von `plugin/admin-dashboard.php` zu `views/admin-dashboard.php`).
  - Entferne `plugin_dir_path(__FILE__) . 'plugin/'` Referenzen.
- [ ] In `blueprint-module.php` (jetzt im Root):
  - Passe Pfade zu Views an.
- [ ] Ersetze hardcodierte Instanzen des Namens "KIW Module Template" durch `{{MODULE_NAME}}`.

### Phase 5: Cleanup
- [ ] Lösche den Ordner `plugin/`.
- [ ] Prüfe `design-system/` (behalte `architecture.md` dort, falls gewünscht - user fragte nur nach `master.md` Verschiebung).
- [ ] Finaler Check aller PHP-Includes.

---

## ✅ Verifizierung
- [ ] Plugin lässt sich in WordPress (theoretisch) noch aktivieren (Header valide trotz Platzhalter?). *Hinweis: WordPress akzeptiert Platzhalter in Headern oft nur bedingt für die Anzeige, aber für das Template ist es korrekt.*
- [ ] Dateistruktur entspricht exakt der KIW-Direktive.
- [ ] `module.json` ist vorhanden und folgt V1 Schema.
