"""
app.py — TikTok Content Strategy Report (Streamlit Community Cloud, free)

Two paths:
  - Cached demo accounts: instant, complete, full-transcription reports. Reliable.
  - Any other account: live analysis from scrape + captions (NO Whisper here,
    because the free container can't run it). Full-transcription reports are
    produced in Colab and dropped into ./cache to become instant demos.

Secrets (app Settings > Secrets, TOML format):
    APIFY_TOKEN = "..."
    GEMINI_KEY = "..."
"""

import os
import streamlit as st
import report_engine as eng

st.set_page_config(page_title="TikTok Strategy Report", page_icon="📊", layout="centered")

DEMO_ACCOUNTS = {
    "vanessaandheriphone": "Spiritual-wellness creator (tarot, hypnotherapy, rituals).",
}

st.title("TikTok Content Strategy Report")
st.caption("Turns a public TikTok account into a client-ready strategy report.")

with st.expander("What this does"):
    st.markdown(
        "- Scrapes a public account's recent videos\n"
        "- Tracks how reach has moved over time\n"
        "- Writes a strategic thesis, content pillars, and sequel ideas\n"
        "- Exports a formatted Word report\n\n"
        "**Demo accounts** return a full report (with transcription) instantly. "
        "**Live analysis** of any other account runs from captions here; the deepest "
        "reports, which read what was actually said in videos, are generated in Colab "
        "and added as demos."
    )

username = st.text_input("TikTok username (no @)", value="vanessaandheriphone")
go = st.button("Generate report", type="primary")

st.write("Or try a demo account (instant, full report):")
cols = st.columns(max(len(DEMO_ACCOUNTS), 1))
for i, (acct, desc) in enumerate(DEMO_ACCOUNTS.items()):
    if cols[i].button(f"@{acct}"):
        username = acct
        go = True


def serve_cached(acct):
    path = os.path.join("cache", f"{acct}.docx")
    if os.path.exists(path):
        with open(path, "rb") as f:
            st.success(f"Loaded the full pre-generated report for @{acct}.")
            st.download_button("Download the Word report", f,
                file_name=f"TikTok_Strategy_{acct}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        return True
    return False


if go and username:
    acct = username.strip().lstrip("@")

    if acct in DEMO_ACCOUNTS and serve_cached(acct):
        st.stop()

    st.info("Running live analysis from scrape and captions. Takes about a minute. "
            "For the deepest report that reads spoken content, use a demo account.")
    bar = st.progress(0.0)
    status = st.empty()

    def setb(frac, msg):
        bar.progress(min(max(frac, 0.0), 1.0)); status.write(msg)

    try:
        setb(0.10, "Scraping the account…")
        df = eng.scrape_account(acct)
        setb(0.45, f"Scraped {len(df)} videos. Analysing…")

        # NO transcription on the cloud container: analyse_and_thesis falls back
        # to captions automatically when there are no transcripts.
        def aprog(done, total, msg):
            setb(0.45 + 0.40 * (done / total), msg)
        S = eng.analyse_and_thesis(df, progress_cb=aprog)

        setb(0.90, "Building the Word document…")
        out = eng.build_document(df, S, out_path=f"report_{acct}.docx")
        setb(1.0, "Done.")

        st.success(f"Report ready for @{acct} (caption-based).")
        with open(out, "rb") as f:
            st.download_button("Download the Word report", f,
                file_name=f"TikTok_Strategy_{acct}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        st.subheader("Preview: the bottom line")
        st.write(S["thesis"]["characterization"] + "  " + S["thesis"]["biggest_mistake"])
        st.subheader("Five things you need to know")
        for f in S["thesis"]["findings"]:
            st.write("• " + f)

    except Exception as e:
        st.error(f"Live analysis failed: {e}")
        st.caption("Live scraping can fail from a shared server. The demo account above always works.")
