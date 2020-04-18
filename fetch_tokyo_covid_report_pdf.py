#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://www.bousai.metro.tokyo.lg.jp/taisaku/saigai/1007261/index.html の
"患者の発生について" （別紙）PDF ファイル、最新のものを "pdf" フォルダにとってくる

新しくとってきたファイルを stdout に出力する。(なければ、何も出さない)
"""

import argparse
from pathlib import Path
import sys
from urllib.parse import urljoin, urlsplit
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bousai.metro.tokyo.lg.jp/taisaku/saigai/1007261/"

REPORT_PAGE_KEYWORD = "新型コロナウイルスに関連した患者の発生について"
APPENDIX_SELECTOR = "li.pdf > a"


def find_latest_report_page(base_url: str):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, "html.parser")

    for a in soup.find_all("a"):
        if REPORT_PAGE_KEYWORD in str(a.string):
            return urljoin(base_url, a.get("href"))
    return ""


def find_latest_report_pdf(report_page_url: str):
    r = requests.get(report_page_url)
    soup = BeautifulSoup(r.content, "html.parser")

    a = soup.select_one(APPENDIX_SELECTOR)
    return urljoin(report_page_url, a.get("href"))


def fetch_pdf(report_pdf_url: str):
    url_path = urlsplit(report_pdf_url).path
    filename = Path(url_path).name
    local_path = Path("pdf") / filename
    # ダウンロード済みかをチェック、すでにファイルがあれば何もしない
    if local_path.exists():
        return ""

    # ダウンロード
    urlretrieve(report_pdf_url, str(local_path))
    return str(local_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('-i', '--int-data', type=int, default=0, help='')
    # parser.add_argument('-b', '--bool-data', action='store_true', help='')
    # parser.add_argument('-c', '--counter', type=int, const=50, nargs='?', help='')
    # parser.add_argument('userid', type=int, help='')
    # parser.add_argument('filenames', nargs='+', help='')
    args = parser.parse_args()

    latest_report_page_url = find_latest_report_page(BASE_URL)
    if not latest_report_page_url:
        sys.exit(1)  # まったくないことはないはず
    # print(latest_report_page_url)

    latest_report_pdf_url = find_latest_report_pdf(latest_report_page_url)
    if not latest_report_pdf_url:
        sys.exit(1)  # まったくないことはないはず
    # print(latest_report_pdf_url)

    local_pdf_path = fetch_pdf(latest_report_pdf_url)

    # ダウンロードした場合、ダウンロードしたファイル名を stdout に出す
    print(local_pdf_path)


if __name__ == '__main__':
    main()
