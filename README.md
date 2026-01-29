# KIW Module Template

Dieses Repository ist ein Template für private KIW WordPress-Module.

## Einmalige Initialisierung nach dem Erstellen eines neuen Repos aus diesem Template

1. Öffne im neuen Repo: **Actions**
2. Starte den Workflow: **"Init Module (set slug + module.json)"**
3. Der Workflow erledigt automatisch:
   - benennt `plugin/` um in `<repo-slug>/`
   - benennt die Hauptdatei um nach `<repo-slug>/<repo-slug>.php`
   - erzeugt `kiw/module.json` (für KIW Suite Auto-Discovery)

## Releases (ZIP-Asset)

- Erstelle einen Tag im Format `vX.Y.Z` (z.B. `v0.1.0`)
- GitHub Actions baut automatisch ein WordPress-ZIP mit genau einem Root-Folder:
  - Asset-Name: `<repo-slug>-vX.Y.Z.zip`
  - ZIP-Root: `<repo-slug>/...`

## Anforderungen für die KIW Suite Auto-Discovery

- `kiw/module.json` muss existieren
- Es muss ein **Latest Release** geben, das ein `.zip` Asset enthält
