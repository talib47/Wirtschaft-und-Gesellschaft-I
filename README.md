# Wirtschaft und Gesellschaft I – Lern-App

Live: https://talib47.github.io/Wirtschaft-und-Gesellschaft-I/

Eine Datei (`index.html`, Vanilla-JS, kein Build-Schritt). Zwei Kurse in einer App, umschaltbar:

- **Ökonomisches Denken** (Seminar, Studienleistung = 4 Quizze): Fragen im Stil einer Fahrschul-App (Einfach-/Mehrfachauswahl, Zuordnen, Zahl), Karteikarten, Quiz-Simulation mit Timer, Bereitschaft je Quiz. Reiter: Übersicht · Üben · Karten · Quiz · Statistik
- **Sozialstruktur** (Vorlesung, Klausur mit Textaufgaben): Karteikarten und Schreibtraining (Antwort schreiben, Erwartungshorizont abhaken, optional Text von Claude bewerten lassen). Reiter: Übersicht · Karten · Üben · Schreiben · Statistik

## Aufbau von `index.html`

| Bereich | Inhalt |
|---|---|
| `<style>` | Design (Farben als Tokens, Dunkelmodus) |
| `BASE` / `BASE_SOZ` | Inhalte: Sitzungen, Fragen, Karten je Kurs |
| `QUIZZES` | Zuordnung der Sitzungen zu den 4 Quizzen |
| `state` | Fortschritt: Fächer `box` und Termine `due` (Karten **und** Fragen), Fehler `err`, Patzer `lapses`, „Wer sagt das?“ `who`, unklare Sitzungen `unclear`, eigene Termine `dates`, echte Quizpunkte `quizPts`, Tageseinheiten `sessions`, Quiz-Simulationen, Entwürfe, Lernzeit |
| `GH` | Geräte-Abgleich über GitHub |
| Textformat | `richText()`, `inl()`, `infoHTML()`, `copyText()` (übernommen aus Wirtschaft II) |
| Lernmethoden | Abruf vor Auswahl (`recallFirst`), Wiederholungsplan `grade`/`gradeCard`/`gradeIdk`, Schreibfeld `drawSurface`, „Wer sagt das?“ `renderWho`, Lexikon `renderLex`, Tageseinheit `planToday`/`sessbar`, Termine `datesBlock`, Schwachstellen `weakBlock` (Ideen aus Wirtschaft II) |
| `render*()` | Ansichten: Home, Üben, Karten, Quiz, Schreiben, Statistik (mit Lern-Tracker) |

## Geräte-Abgleich

- **Offline:** `sw.js` speichert die App-Dateien im Gerät. Die App startet auch ohne Internet (Netz höchstens 3 Sekunden, sonst die gespeicherte Kopie). Der Lernstand liegt immer zuerst im Gerät (`localStorage`) und wird abgeglichen, sobald wieder Internet da ist. Beim Abgleich gewinnt der neuere Stand als Ganzes: Wer offline auf zwei Geräten lernt, verliert den Stand des älteren.

- Fortschritt liegt als `fortschritt.json` im Zweig `fortschritt` dieses Repos (GitHub-Contents-API).
- Gerät verbinden: `https://talib47.github.io/Wirtschaft-und-Gesellschaft-I/#t=<GitHub-Schlüssel>` einmal öffnen.
- Eigene Schlüssel pro App: `od-lernapp-v1`, `od-gh-token`, `od-zoom`.

Schwester-App mit modularem Aufbau, Wiederholungsplan wie bei Anki, Rechentrainer und Probeklausur: https://github.com/talib47/Wirtschaft-II

## So kommen neue Sitzungen dazu

Gilt für jeden Chat, der neue Folien einbaut. Grundlage sind nur die Folien. Nichts dazuerfinden. Widerspricht etwas der Folie, gilt die Folie, mit kurzem Hinweis (im `i`-Feld der Karte oder in der Antwort an Talib).

**Wichtig für den Lernstand:** IDs nie ändern, nie wiederverwenden. Die Schlüssel `od-lernapp-v1`, `od-gh-token`, `od-zoom` und die Datei `fortschritt.json` bleiben unverändert. Nur neue Einträge anhängen, nichts löschen.

### ID-Schema

| Was | Ökonomisches Denken (`BASE`) | Sozialstruktur (`BASE_SOZ`) |
|---|---|---|
| Sitzung | `BASE.sitzungen["2"]="Age of Religion"` | `BASE_SOZ.sitzungen["2"]="Titel (22.10.)"` |
| Frage | `s2-01`, `s2-02` … | – |
| Karte | `s2-k01` … | `soz2-k01` … |
| Schreibaufgabe | – | `soz2-a01` … |

### Aufbau einer Lektion (= eine Sitzung)

- **Ökonomisches Denken:** 30–40 Fragen im Moodle-Stil, davon 20–30 % andere Typen (Mehrfachauswahl, Zuordnung, Zahl), dazu 15–20 Karten. Rechenstoff immer auch als Zahlenfrage.
- **Sozialstruktur:** 20–25 Karten und 5–7 Schreibaufgaben mit Operator (Erläutern, Vergleichen, Beschreiben …).
- Reihenfolge der Folien beibehalten. Quiz-Zuordnung steht in `QUIZZES` (Quiz 1 = Sitzung 1–4, 2 = 5–7, 3 = 8–10, 4 = 11–12).

### Fragen (Pflicht: Begründung für jede falsche Antwort)

```js
{id:"s2-01", s:2, q:"Frage", o:["RICHTIG zuerst","falsch A","falsch B","falsch C"], e:"Warum die richtige Antwort stimmt",
 w:{1:"Warum A falsch ist und was den Unterschied macht", 2:"…", 3:"…"}}
```
- Die richtige Antwort steht in `o` immer an erster Stelle, die App mischt.
- `w` ist **Pflicht**: für jeden falschen Index ein Satz, warum genau diese Wahl falsch ist (Verwechslung benennen, z. B. „Das ist Platon, nicht Xenophon“).
- Richtig/Falsch: `o:["Falsch","Richtig"], a:0, fix:true, w:{1:"…"}` (Index der richtigen in `a`).
- Mehrfachauswahl: `typ:"multi", o:[…], a:[0,2], w:{3:"…"}` (Begründung für jede falsche Option).
- Zuordnung: `typ:"zuord", paare:[["Begriff","Zuordnung"], …]` (4–6 Paare), `e` mit Eselsbrücke.
- Zahl: `typ:"zahl", a:400, einheit:"%", tol:0, e:"Rechenweg", w:"typischer Fehler"`.

### Karten

```js
{id:"s2-k01", s:2, ctx:"Kontextzeile: worum es geht", f:"Begriff oder Frage", b:"Rückseite", i:"Herkunft oder Eselsbrücke"}
```
- `ctx` (Pflicht): kurze Zeile über der Frage, z. B. „Geld, Wert und gerechter Tausch“ oder „Konzept“.
- `b` gegliedert schreiben, nicht als Fließtext:
  - `- ` Aufzählung, `1. ` Ablauf
  - `Begriff: Erklärung` → Begriff fett (Begriff höchstens 42 Zeichen)
  - `$ (Ertrag − Kosten) / Kosten` → Formelbox
  - Vergleich als Tabelle, erste Spalte = Zeilenkopf: `| | A | B` dann `| Merkmal | … | …` (auf dem Handy gestapelt)
  - `**fett**` für Kernbegriffe; Fachbegriff in Klammern dahinter wird automatisch leiser gesetzt
  - Zahl und Einheit mit normalem Leerzeichen schreiben („40 €“), die App hält sie zusammen
- `i` (optional, dezent): Wortherkunft, Eselsbrücke oder Hinweis auf einen Widerspruch in den Folien.

### Schreibaufgaben (Sozialstruktur)

```js
{id:"soz2-a01", s:2, q:"Erläutern Sie …", k:["Kriterium = 1 Punkt", …], m:"1) **Kern:** …\n2) …"}
```
- `k`: 5–8 Kriterien, je 1 Punkt.
- `m`: gegliedert mit `1) 2) 3)`, Kernbegriffe **fett**. Echte Essays dürfen Fließtext bleiben: dann `essay:true` setzen.

### Prüfen vor dem Hochladen

1. `node --check` auf das Skript.
2. Keine doppelten IDs (Fragen, Karten, Aufgaben).
3. Headless-Browser, hell und dunkel, Handybreite 320–390 px: keine JS-Fehler, nichts ragt über den Rand.
4. Commit als `Claude <noreply@anthropic.com>`, push auf `main`. Den Zweig `fortschritt` nie anfassen.

### Beispielboxen in Karten

Zeilen mit `> ` werden zu einer Box mit Label links, z. B.
```
> Ertrag: 20 €
> Kosten: 5 €
> Rendite: (20 − 5) / 5 = 300 %
```
Überschrift statt „Beispiel“: erste Zeile `> [Fall]`.

### „Wer sagt das?“ (Pflicht: 8–15 Aussagen pro Sitzung)

```js
// in BASE.wer bzw. BASE_SOZ.wer
{id:"s2-w01", s:2, t:"Sinngemäße Aussage nach der Folie", a:"schluessel", alt:["auch_vertretbar"],
 ex:"Begründung, warum es zu a gehört", w:{andererSchluessel:"Warum genau diese Verwechslung falsch ist"}}
```
- `t` ist **sinngemäß** formuliert, kein erfundenes Zitat. Nur Aussagen, die so auf den Folien stehen.
- `a` muss in `werListe` stehen. Neue Autoren, Theorien oder Ansätze dort ergänzen (Schlüssel nie umbenennen). In `BASE_SOZ.werListe` mit Gruppe `g` (`theorie`, `ansatz`, `bild`): Falschantworten kommen zuerst aus derselben Gruppe.
- `alt`: Schlüssel, die ebenfalls vertretbar wären. Sie werden nicht als falsche Antwort angeboten.
- `w`: für typische Verwechslungen eine Begründung.
- IDs: `s2-w01` (Ökonomisches Denken), `soz2-w01` (Sozialstruktur).

### Was die App beim Lernen macht (nicht ändern ohne Grund)

- Fragen: Bei Einfach- und Mehrfachauswahl erst selbst abrufen, dann „Auswahl zeigen“. Ausnahmen: Richtig/Falsch, Zuordnung, Zahl und Fragen mit „NICHT“.
- Wiederholungsplan für Karten **und** Fragen: 0, 0, 1, 3, 7, 16, 35 Tage. Karten mit drei Stufen (Nicht gewusst / Unsicher / Sicher). „Weiß ich nicht“ ohne Strafe: Fach bleibt, kein Fehler, kommt in der Runde und morgen wieder.
- Beim Start wird **nichts** gespeichert (sonst überschreibt der Abgleich einen neueren Stand). `norm()` ergänzt fehlende Termine nur im Speicher.
- Die Quiz-Simulation bleibt wie Moodle: Auswahl sofort sichtbar, kein „Weiß ich nicht“.

## Updates

Nach jeder Änderung an `index.html` einmal `python3 stamp.py` ausführen: setzt die Versionsnummer im Update-Check und schreibt `version.txt`. Die App vergleicht beim Start und beim Zurückkehren ihre Version damit und lädt sich bei Änderungen neu.
