#!/usr/bin/env python3
import os
import math
import time
import csv
import argparse
import logging
import json
import yaml
from typing import Dict, List, Optional

import requests
import matplotlib.pyplot as plt

ADS_API = "https://api.adsabs.harvard.edu/v1/search/query"
GOOGLE_API = "https://www.googleapis.com/customsearch/v1"

logger = logging.getLogger("research_presence")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_config(path: str) -> Dict[str, str]:
    """Load API credentials from a YAML or JSON config file."""
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".json"):
            return json.load(f)
        else:
            return yaml.safe_load(f)

def ads_count_papers(author: str, token: str,
                     refereed: bool = False,
                     aff: Optional[str] = None,
                     year_range: Optional[str] = None,
                     orcid: Optional[str] = None,
                     delay: float = 0.2) -> int:
    """Return the number of ADS records matching the query."""
    headers = {"Authorization": f"Bearer {token}"}
    clauses = [f'author:"{author}"', "collection:astronomy"]
    if refereed:
        clauses.append("property:refereed")
    if aff:
        clauses.append(f'aff:"{aff}"')
    if year_range:
        clauses.append(f"year:{year_range}")
    if orcid:
        clauses.append(f"orcid:{orcid}")
    q = " AND ".join(clauses)
    params = {"q": q, "rows": 0, "fl": "id"}
    resp = requests.get(ADS_API, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    num = int(resp.json()["response"]["numFound"])
    time.sleep(delay)
    return num

def google_total_results(query: str, api_key: str, cx: str, delay: float = 1.0) -> int:
    """Return approximate number of Google results using the Programmable Search API."""
    params = {"key": api_key, "cx": cx, "q": query}
    resp = requests.get(GOOGLE_API, params=params, timeout=30)
    if resp.status_code != 200:
        logger.warning("Google API error %s for %r: %s",
                       resp.status_code, query, resp.text[:200])
        return 0
    data = resp.json()
    total = int(data.get("searchInformation", {}).get("totalResults", "0"))
    time.sleep(delay)
    return total

def load_names(path: str) -> List[str]:
    """Read researcher names from TXT or CSV file."""
    names = []
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("name"):
                    names.append(row["name"].strip())
    else:
        with open(path, encoding="utf-8") as f:
            for line in f:
                n = line.strip()
                if n and not n.startswith("#"):
                    names.append(n)
    return names

def write_csv(rows: List[Dict], out_csv: str):
    """Write results to CSV file."""
    fieldnames = ["name", "ads_papers", "google_results"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def make_plot(rows: List[Dict], out_png: str):
    """Make anonymized log–log scatter plot."""
    xs, ys = [], []
    for r in rows:
        a = int(r["ads_papers"])
        g = int(r["google_results"])
        xs.append(math.log10(a + 1))
        ys.append(math.log10(g + 1))
    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, alpha=0.7)
    plt.xlabel("log10(ADS papers + 1)")
    plt.ylabel("log10(Google hits + 1)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--names", required=True, help="Path to TXT or CSV file with column 'name'")
    ap.add_argument("--config", required=True, help="Path to config.yaml or config.json")
    ap.add_argument("--out_csv", default="output.csv")
    ap.add_argument("--out_png", default="scatter.png")
    ap.add_argument("--ads_refereed", action="store_true")
    ap.add_argument("--ads_aff", default=None)
    ap.add_argument("--ads_year", default=None)
    args = ap.parse_args()

    cfg = load_config(args.config)
    ads_token = cfg["ads_token"]
    gkey = cfg.get("google_api_key")
    gcx = cfg.get("google_cx")

    names = load_names(args.names)
    results = []
    for name in names:
        logger.info("Processing %s", name)
        try:
            ads_count = ads_count_papers(name, ads_token,
                                         refereed=args.ads_refereed,
                                         aff=args.ads_aff,
                                         year_range=args.ads_year)
        except Exception as e:
            logger.error("ADS error for %s: %s", name, e)
            ads_count = 0
        gcount = google_total_results(f"{name} astronomy", gkey, gcx) if gkey and gcx else 0
        results.append({"name": name, "ads_papers": ads_count, "google_results": gcount})

    write_csv(results, args.out_csv)
    make_plot(results, args.out_png)
    logger.info("Done. Wrote %s and %s", args.out_csv, args.out_png)

if __name__ == "__main__":
    main()
