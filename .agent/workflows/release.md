---
description: KI-WERKE Professional Release Workflow v1.1.0
---

---
description: KI-WERKE Professional Release Workflow v1.1.0
---

# /release

1. **Architecture-Audit (Linter):**
   - Rufe den Skill `architecture-linter` auf.
   - Prüfe auf CDN-Links, fehlendes Escaping und ungesicherte Inputs.
   - Brich bei Verstößen sofort ab.

2. **Integrity-Check (Self-Destruct):**
   - Validiere die `checksums.json` gegen den aktuellen Datei-Stand.
   - Stelle sicher, dass `src/Utils/SelfDestruct.php` aktiv eingebunden ist.

3. **Versioning (module.json):**
   - Lese `system.cms` und `version` aus der `module.json`.
   - Inkrementiere die Version (Patch-Level) im JSON und im Plugin-Header.

4. **Document-Sync:**
   - Extrahiere die neuesten Änderungen aus der `walkthrough.md`.
   - Bereite die Release-Notes für GitHub vor.

5. **Git & GitHub Execution:**
   - `git add .`
   - `git commit -m "Build v{{version}} [Security Hardened]"`
   - `git tag -a v{{version}} -m "KI-WERKE Release v{{version}}"`
   - `gh release create v{{version}} --title "v{{version}}" --notes-file walkthrough.md`

6. **Zentrale-Hash:**
   - Generiere den finalen SHA-256 Hash des Releases.
   - Gib den Hash aus, damit dieser als "autorisierter Build" für die KI Werke Zentrale registriert werden kann.