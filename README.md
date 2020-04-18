# parse-tokyo-covid-report-pdf

https://www.bousai.metro.tokyo.lg.jp/taisaku/saigai/1007261/index.html の "患者の発生について" （別紙）から、区ごとの発生状況を読み取り、カンマ区切りで出力します。

## 自動生成データ

GitHub Actions を利用して [csv/latest.csv](csv/latest.csv) から最新の情報がとれるようにしました。raw ファイルは https://raw.githubusercontent.com/smatsumt/parse-tokyo-covid-report-pdf/master/csv/latest.csv にて取得可能です。

過去 csv も [csv](csv) フォルダにありますので、必要に応じてご参照ください。

## Usage

```shell script
# 最初の1回のみ
pip3 install -r requirements.txt
```

```
./parse_tokyo_covid_report_pdf.py 20200411.pdf
# 千代田,10
# 中央,33
# 港,143
...
```
