# Champions-of-History
What if the most famous figures across time came together for a tournament unlike any other? With over 2,000 participants, this tournament thrusts history's most impactful people into the spotlight to crown a champion.

Participants were chosen from Wikipedia's vital articles list. The Level 4 section lists 2,000 articles under its "Poeple" section. The invited participants in "Invitees.txt" which fill out the rest of the field were chosen by a variety of criteria, including social media follwing on various platforms and artificial intelligence suggestions.
 
Project layout
------------
- `src/`: Python package with main modules (`src/main.py`, `src/preparation.py`, `src/scrape.py`, `src/utils.py`).
- `scripts/`: Runnable helper scripts (e.g. `scripts/generate_bracket.py`).
- `data/`: Input JSON/CSV/TXT files (`participants.json`, `regions.csv`, `invitees.csv`, etc.).
- `templates/`: HTML templates used to render the bracket (`BracketTop.html`, `Bracket.html`).
- `outputs/`: Generated artifacts (PDF/HTML) produced by the scripts.

Quick run instructions
----------------------
Use the project's virtual environment to run scripts. From the repository root (PowerShell examples):

Run a short simulation (CLI-safe):
```powershell
.venv\Scripts\python.exe -m src.main
```

Generate the printable bracket PDF (requires `weasyprint` and its dependencies):
```powershell
.venv\Scripts\python.exe scripts\generate_bracket.py
```

If `weasyprint` or other Python packages are not installed in the venv, install them with:
```powershell
.venv\Scripts\python.exe -m pip install pandas weasyprint wikipediaapi beautifulsoup4 requests
```

Notes
-----
- The code resolves files from `data/` by default but will fall back to root paths if data hasn't been moved.
- `src` is a package; run modules with `-m` when possible for reliable imports.
- Generating PDFs with `weasyprint` may require OS-level libraries (cairo, pango). If PDF generation fails, the script will still write the HTML into `outputs/` so you can convert externally.
