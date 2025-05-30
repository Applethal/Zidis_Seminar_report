# Zidis_Seminar_report


# Survey Report Generator

Ein Python-Tool zur automatischen Erstellung von den Seminare-Feedback in LaTeX format aus CSV-Umfragedaten.

## Überblick

Dieses Skript verarbeitet heruntergeladene CSV-Dateien mit Umfrageergebnissen und erstellt automatisch einen strukturierten LaTeX-Bericht. Die Antworten werden nach Kategorien gebündelt und als PDF-Dokument ausgegeben.

## Systemanforderungen
Bitte installieren: 
### Python-Abhängigkeiten 
- Python 3.6 oder höher
- pandas
- pathlib (standardmäßig in Python 3.4+ enthalten)

### LaTeX-Installation
Für die automatische PDF-Erstellung benötigen Sie eine LaTeX-Distribution:

**Windows:**
- MiKTeX: https://miktex.org/download
- TeX Live: https://www.tug.org/texlive/

**macOS:**
- MacTeX: https://www.tug.org/mactex/

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-lang-german
```

**Linux (CentOS/RHEL/Fedora):**
```bash
sudo yum install texlive-latex texlive-collection-langeuropean
# oder für neuere Versionen:
sudo dnf install texlive-latex texlive-collection-langeuropean
```

## Installation

1. **Python-Pakete installieren:**
```bash
pip install pandas
```

2. **LaTeX-Distribution installieren** (siehe Systemanforderungen oben)

3. **Skript herunterladen** und in den gewünschten Ordner kopieren

## Verwendung

### Vorbereitung der CSV-Dateien

Ihre CSV-Dateien müssen folgende Spalten enthalten (Sie sind schon in den Datein rein. Bitte nur zur Sicherheit prüfen):
- `Das war gut:`
- `Das würde ich mir noch wünschen:`
- `Folgende Themen und Tools fand ich besonders nützlich:`

**Wichtige Hinweise:**
- CSV-Dateien sollten mit Semikolon (`;`) als Trennzeichen formatiert sein
- Das Skript unterstützt verschiedene Textcodierungen (UTF-8, Windows-1252, ISO-8859-1)
- Leere Zellen und Zellen mit "[BILD]" werden automatisch ignoriert

### Ausführung

1. **CSV-Dateien in den Skript-Ordner kopieren**
   - (WICHTIG!) Alle CSV-Dateien sollten im selben Verzeichnis wie das Python-Skript liegen. 

2. **Skript ausführen:**
```bash
python survey_report_generator.py
```

3. **Ausgabe:**
   - `survey_report.tex` - LaTeX-Quelldatei
   - `survey_report.pdf` - Fertig kompilierter Bericht (falls LaTeX verfügbar)

### Anpassbare Parameter

Sie können das Skript durch Änderung folgender Variablen in der `main()`-Funktion anpassen:

```python
folder_path = "."  # Pfad zu den CSV-Dateien
output_file = "survey_report.tex"  # Name der Ausgabedatei
```

## Ausgabeformat

Der generierte Bericht enthält:

1. **Titelseite** mit Autor und Datum
2. **Inhaltsverzeichnis**
3. **Kategoriebasierte Abschnitte:**
   - Das war gut
   - Das würde ich mir noch wünschen
   - Folgende Themen und Tools fand ich besonders nützlich

Jeder Abschnitt zeigt:
- Anzahl der Antworten in dieser Kategorie
- Alle Kommentare als Aufzählungsliste
- Quelldatei-Referenz für jeden Kommentar (in grau)

## Fehlerbehebung

### "pdflatex not found" Fehler
- Stellen Sie sicher, dass LaTeX installiert ist
- Überprüfen Sie, ob `pdflatex` in Ihrem PATH verfügbar ist
- Testen Sie: `pdflatex --version` in der Kommandozeile

### Encoding-Probleme bei CSV-Dateien
Das Skript versucht automatisch verschiedene Textcodierungen:
- UTF-8
- Windows-1252
- ISO-8859-1
- CP1252
- Latin1

Wenn Probleme auftreten, speichern Sie die CSV-Datei als UTF-8.

### Fehlende Spalten
Das Skript gibt Warnungen aus, wenn erwartete Spalten nicht gefunden werden:
```
Warning: Column 'Das war gut:' not found in datei.csv
```

### Manuelle PDF-Erstellung
Falls die automatische Kompilierung fehlschlägt:
```bash
pdflatex survey_report.tex
pdflatex survey_report.tex  # Zweimal für korrektes Inhaltsverzeichnis
```

## Beispiel-Ausgabe

```
Processing: umfrage_gruppe1
Processing: umfrage_gruppe2
Processing: umfrage_gruppe3
LaTeX document generated successfully: survey_report.tex
Processed 3 CSV files
Compiling survey_report.tex to PDF...
PDF successfully generated: survey_report.pdf
Report generation and compilation completed successfully!
```

## Dateierweiterungen und Bereinigung

Das Skript erstellt temporäre LaTeX-Dateien:
- `.aux` - Hilfsdatei
- `.log` - Kompilierungsprotokoll
- `.toc` - Inhaltsverzeichnis-Daten

Diese können nach erfolgreicher PDF-Erstellung gelöscht werden.

## Support
Einfach mal mich über nordine@rptu.de kontaktieren!


