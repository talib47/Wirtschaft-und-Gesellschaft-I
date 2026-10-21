# Wirtschaft und Gesellschaft I – Lern-App

Live: https://talib47.github.io/Wirtschaft-und-Gesellschaft-I/

Eine Datei (`index.html`, Vanilla-JS, kein Build-Schritt). Zwei Kurse in einer App, umschaltbar:

- **Ökonomisches Denken** (Seminar, Studienleistung = 4 Quizze): Fragen im Stil einer Fahrschul-App (Einfach-/Mehrfachauswahl, Zuordnen, Zahl), Karteikarten, Quiz-Simulation mit Timer, Bereitschaft je Quiz. Reiter: Übersicht · Üben · Karten · Quiz · Statistik
- **Sozialstruktur** (Vorlesung, Klausur mit Textaufgaben): Karteikarten und Schreibtraining (Antwort schreiben, Erwartungshorizont abhaken, optional Text von Claude bewerten lassen). Reiter: Übersicht · Karten · Schreiben · Statistik

## Aufbau von `index.html`

| Bereich | Inhalt |
|---|---|
| `<style>` | Design (Farben als Tokens, Dunkelmodus) |
| `BASE` / `BASE_SOZ` | Inhalte: Sitzungen, Fragen, Karten je Kurs |
| `QUIZZES` | Zuordnung der Sitzungen zu den 4 Quizzen |
| `state` | Fortschritt (Leitner-Boxen `box`, Quiz-Ergebnisse, Entwürfe, Lernzeit) |
| `GH` | Geräte-Abgleich über GitHub |
| `render*()` | Ansichten: Home, Üben, Karten, Quiz, Schreiben, Statistik (mit Lern-Tracker) |

## Geräte-Abgleich

- Fortschritt liegt als `fortschritt.json` im Zweig `fortschritt` dieses Repos (GitHub-Contents-API).
- Gerät verbinden: `https://talib47.github.io/Wirtschaft-und-Gesellschaft-I/#t=<GitHub-Schlüssel>` einmal öffnen.
- Eigene Schlüssel pro App: `od-lernapp-v1`, `od-gh-token`, `od-zoom`.

Schwester-App mit modularem Aufbau, Wiederholungsplan wie bei Anki, Rechentrainer und Probeklausur: https://github.com/talib47/Wirtschaft-II
