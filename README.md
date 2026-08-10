# TikTok Content Strategy Report — Complete Setup

This package has two parts:

1. **colab/generate_report.py** — the full pipeline (scrape, transcribe, thesis,
   trend, Word report). Run this in Google Colab to GENERATE reports. Each report
   it makes becomes an instant demo in the app.

2. **streamlit-app/** — the web app you deploy for a shareable URL. It serves
   pre-generated reports instantly (no cost) and can do lighter live analysis.

You have new Apify and Gemini keys. Below is the full setup on a fresh laptop.

---------------------------------------------------------------------------
## PART A — Generate a report in Colab (do this first)
---------------------------------------------------------------------------

1. Go to https://colab.research.google.com  and start a New notebook.
2. Runtime > Change runtime type > Hardware accelerator: T4 GPU > Save.
3. Open  colab/generate_report.py  from this package, copy ALL of it, paste
   into the Colab cell.
4. Near the top, fill in three things:
      APIFY_TOKEN = "your new apify token"
      GEMINI_KEY  = "your new gemini key"
      ACCOUNT     = "the_account_to_analyse"   (no @)
5. Press the play button. It scrapes, transcribes (a few minutes), writes the
   report, and downloads  <account>.docx  to your computer.
6. Repeat for each account you want as a demo (change ACCOUNT, run again).

Cost note: each report downloads ~18 videos via Apify, which uses some credit.
Lower TRANSCRIBE_CAP (e.g. to 10) to spend less per report.

---------------------------------------------------------------------------
## PART B — Deploy the web app (shareable URL)
---------------------------------------------------------------------------

### B1. Put your cached reports into the app
- For each  <account>.docx  you generated, copy it into  streamlit-app/cache/
- Open  streamlit-app/app.py , find the DEMO_ACCOUNTS block near the top, and
  add a line for each account, for example:
      DEMO_ACCOUNTS = {
          "vanessaandheriphone": "Spiritual-wellness creator.",
          "youraccount2": "Short description.",
      }
- The cache filename MUST match the account name exactly: cache/youraccount2.docx

### B2. Put the app on GitHub
1. Go to https://github.com  , sign in (or sign up).
2. Click New (new repository). Name it, set Private, do NOT add a README.
   Create repository.
3. Click "uploading an existing file".
4. Drag in the CONTENTS of the streamlit-app folder:  app.py, report_engine.py,
   requirements.txt, AND the cache folder (with the .docx files inside it).
   IMPORTANT: the cache folder must upload as a folder. After upload, confirm
   you see  cache/vanessaandheriphone.docx  (a cache FOLDER containing the doc),
   NOT the .docx sitting loose at the top level. If it landed loose, rename it
   to  cache/vanessaandheriphone.docx  to move it into the folder.
5. Commit changes.

### B3. Deploy on Streamlit
1. Go to https://share.streamlit.io  , sign in with GitHub, authorize it.
2. Create app > Deploy a public app from GitHub.
3. Repository: your repo. Branch: main. Main file path: app.py
4. Click Advanced settings > Secrets, paste (with your new keys):
      APIFY_TOKEN = "your new apify token"
      GEMINI_KEY = "your new gemini key"
5. Deploy. Wait a few minutes. You get a public URL.

### B4. Test
- Click a demo button. It should load the report instantly (no keys needed).
- Type a new account + Generate to test live analysis (uses Apify credit).

---------------------------------------------------------------------------
## Honest notes
---------------------------------------------------------------------------
- Demo (cached) reports cost NOTHING to show and never fail. Use these for the
  team demo. Pre-cache any account you want to show.
- Live analysis on Streamlit is caption-based (no Whisper there) and uses Apify
  credit. It can fail from a shared server. It is the backup, not the showcase.
- Full-quality reports (with transcription) come from the Colab pipeline.
- If live analysis says "APIFY_TOKEN not set", your Secrets did not save; redo B3.4.
- If a demo button scrapes instead of loading instantly, the cache file is in the
  wrong place or misnamed; see B2.4.
