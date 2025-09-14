# 📊 Researcher Presence Script

This repository provides a Python script to measure the balance between **scientific impact** and **internet presence** of researchers.  

It uses:
- **NASA ADS API** to count the number of refereed papers per author.  
- **Google Programmable Search API** to estimate the number of Google results for `"<Name> astronomy"`.  
- A **scatter plot** (log–log) to visualize the relationship.  
- Output in CSV and PNG formats.

---

## 🚀 Features

- Input: plain text or CSV file with researcher names.  
- Output:  
  - CSV with each researcher’s paper count (ADS) and approximate Google result count.  
  - Scatter plot with anonymized dots (no names).  
- Config file (`config.yaml` or `config.json`) stores all credentials safely.  
- Options to restrict ADS searches by year, affiliation, or refereed status.

---

## 🛠 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/researcher-presence.git
cd researcher-presence
pip install -r requirements.txt
```

---

## 🔑 Getting the Credentials

1. ADS Token (for NASA Astrophysics Data System)

 * Create an account at [ADS](https://ui.adsabs.harvard.edu/)
 * Go to Settings → API Token.
 * Click Generate a new key.
 * Copy the token string (looks like abcd1234...).
 * Paste it into your config.yaml file under ads_token.

2. Google API Key

 * Go to [Google Cloud Console](https://console.cloud.google.com/welcome)
 * Create or select a project.
 * In the sidebar, go to APIs & Services → Library.
 * Search for Custom Search API and click Enable.
 * Go to APIs & Services → Credentials.
 * Click Create Credentials → API key.
 * Copy the generated key (string like AIzaSy...).
 * Paste it into your config.yaml file under google_api_key.

3. Google CX (Search Engine ID)

 * Go to the [Programmable Search Engine Control Panel](https://programmablesearchengine.google.com/controlpanel/all)
 * Click Add to create a new search engine.
 * In Sites to Search, you can start with www.google.com (then edit settings).
 * Once created, go to the Setup tab.
 * Copy the Search engine ID (string like 0123456789:abcdef).
 * Paste it into your config.yaml file under google_cx.
 * In the control panel → Setup → Basics, set it to Search the entire web.

---

⚙️ Configuration

Example config.yaml:

```yaml
ads_token: "YOUR_ADS_TOKEN"
google_api_key: "YOUR_GOOGLE_API_KEY"
google_cx: "YOUR_GOOGLE_CX"
```

---

📂 Input File Format
Option A: Text file (researchers.txt)
```txt
Rashid Sunyaev
Vera Rubin
Michel Mayor
Jocelyn Bell
```

Option B: CSV file (researchers.csv)
```csv
name
Rashid Sunyaev
Vera Rubin
Michel Mayor
Jocelyn Bell
```

---

▶️ Usage

```bash
python script.py --names researchers.txt --config config.yaml --ads_refereed --ads_year 2000-2025
```

Options

 * `--names`: Path to TXT or CSV with researcher names.
 * `--config`: Path to config file (.yaml or .json).
 * `--out_csv`: Name of the CSV output file (default: output.csv).
 * `--out_png`: Name of the plot PNG file (default: scatter.png).
 * `--ads_refereed`: Restrict ADS results to refereed papers only.
 * `--ads_aff`: Filter ADS results by affiliation (e.g., "Cambridge").
 * `--ads_year`: Restrict to a year range, e.g. 2000-2025.

---

📊 Outputs

output.csv

```
name,ads_papers,google_results
Rashid Sunyaev,250,18200
Vera Rubin,180,20900
Michel Mayor,320,15500
Jocelyn Bell,140,9500
```


scatter.png
A log–log scatter plot of ADS papers vs Google results (points only, no labels).

---

📝 License

MIT License — feel free to use, modify, and share.
