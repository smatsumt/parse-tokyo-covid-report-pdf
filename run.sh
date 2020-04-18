#!/usr/bin/env bash

# PDF をとってくる
NEW_PDF_FILE=$(./fetch_tokyo_covid_report_pdf.py)
if [[ -z "${NEW_PDF_FILE}" ]] ;then
  echo "No new PDF. exited"
  exit 255
fi

# PDF から CSV を生成
NEW_CSV_FILE=${NEW_PDF_FILE//pdf/csv}
./parse_tokyo_covid_report_pdf.py ${NEW_PDF_FILE} > ${NEW_CSV_FILE}

# もしファイル名の末尾に数字がついていたら、日付のみの csv も作る
DAY_CSV_FILE=${NEW_CSV_FILE:0:12}.csv
if [[ ${NEW_CSV_FILE} != ${DAY_CSV_FILE} ]]; then
  cp "${NEW_CSV_FILE}" "${DAY_CSV_FILE}"
fi

# latest.csv のコピーを生成
cp "${NEW_CSV_FILE}" csv/latest.csv
