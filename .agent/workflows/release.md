# KI-WERKE Release Workflow (v1.1.2)
Dieses Dokument erzwingt eine atomare Release-Kette. Schlägt ein Schritt fehl, wird das gesamte Release abgebrochen.

## 1. Pre-Flight Check (Linter)
- Führe den `architecture-linter` aus.
- Prüfe auf CDN-Links, fehlendes Escaping und harte Credentials.
- Abbruch bei Fehlern.

## 2. Versionierung & Hashing
- Erhöhe die Version in `module.json`.
- Berechne SHA-256 Hash über `src/` und `module.json`.
- Aktualisiere die lokale `release.md`.

## 3. GitHub Automatisierung (Vollautomatisch)
- Führe `git add .` aus.
- Commit: "Release v[VERSION] - Architecture v1.1.2".
- Tag: Erstelle lokalen Tag `v[VERSION]`.
- Push: Sende Branch und Tag zu `kiwerkepro-org` auf GitHub.

## 4. Cloud-Registrierung (Vollautomatisch)
- Lade `KIW_CENTRAL_USER` und `KIW_CENTRAL_PASS` aus `.env`.
- Sende POST an `https://zentrale.kiwerke.com/api/v1/register`.
- JSON Payload: `{ "module": "[SLUG]", "version": "[VERSION]", "hash": "[HASH]" }`.

## 5. Abschlussbericht
- Bestätige (a) GitHub-Status, (b) Tag-Status, (c) Zentrale-Status.