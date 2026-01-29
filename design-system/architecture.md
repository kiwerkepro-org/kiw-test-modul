# Architektur-Richtlinien (Architecture)

Dieses Dokument definiert die technischen Standards für die Code-Qualität und Systemarchitektur innerhalb dieses Moduls. Es fungiert als oberste Instanz neben der `master.md`.

## 🎨 UI & Styling
- **Tailwind CSS:** Alle UI-Komponenten müssen konsequent Tailwind-Utility-Classes nutzen. Ad-hoc CSS ist zu vermeiden.
- **Icons:** Nutze für alle Icons ausschließlich **Lucide-SVG-Icons**. Die Verwendung von Font-Awesome oder Emojis ist untersagt.

## 🏗️ Code-Struktur
- **Seperation of Concerns:** PHP-Dateien müssen strikt in **Logic** (Controller/Business Logic) und **View** (HTML/Template) getrennt sein.
- **Dokumentation:** Jede Funktion muss mit einem standardisierten DocBlock versehen sein, der den Zweck, Parameter und Rückgabewerte erklärt.

## ⚖️ Compliance & Qualität
- Dieses Dokument ist die oberste Instanz für Code-Qualität neben der `master.md`.
- Alle Änderungen müssen gegen diese Regeln geprüft werden.
