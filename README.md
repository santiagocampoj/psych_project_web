# Psychoacoustic Rating Task

## What you need

- **Python 3** installed → if you don't have it: <https://www.python.org/downloads/> (any recent version works)
- 10 minutes

## Step 1 — Download the project

Download the zip file from Santi.

Unzip wherever you want — Desktop is fine. You'll get a folder like `psych_project_web`.

## Step 2 — Open a terminal in that folder

**Windows**
1. Open the unzipped folder in File Explorer.
2. Click the address bar at the top, type `cmd`, press Enter. A black terminal opens already pointing to the right folder.

**Mac**
1. Open Terminal (`Cmd+Space`, type "Terminal", Enter).
2. Type `cd ` (with a space) and then drag the unzipped folder into the terminal. Press Enter.

**Linux**
You know what to do.

## Step 3 — Start the local server

In the terminal, run:

```bash
python -m http.server 8000
```

If that says "command not found", try `py -m http.server 8000` (Windows) or `python3 -m http.server 8000` (Mac/Linux).

You should see something like:

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**Leave this window open** for the entire test. Closing it stops the server.

## Step 4 — Open the rating page

In any browser, go to:

<http://[::1]:8000/psych_project_web/> or your port.

## Step 5 — Do the test

3. For each block: listen to the **reference audio** (highlighted in yellow) first, then each modified version.
4. Rate each modification on the two scales (1–7).
5. When all ratings are done, click **"Download my results"**. A CSV file will save to your Downloads folder.ç

## Can't run the server? No problem.

Alternative: use the manual CSV template.

1. Open `rating_template.csv` in Excel / Numbers / Google Sheets.
2. Listen to the audio files directly from `data/stimuli/` (just double-click them).
3. Fill in your ratings (1–7) in the `consonance` and `pleasantness_vs_ref` columns.
4. Save and send me the file.

The audio files are short (5 seconds each, ~40 MB total for all 32 stimuli).

## Step 6 — Send me the CSV

Send the downloaded file (named like `YourInitialHere.csv`) to:

That's it! Thank you.

---