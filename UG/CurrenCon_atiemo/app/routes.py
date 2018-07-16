import os
from flask import Flask, render_template, request
import requests
import json
import xlrd

app = Flask(__name__)


currencies_d = {}
wb = xlrd.open_workbook('currency_list.xls')
sh = wb.sheet_by_index(0)

for i in range(156):
    code = str(sh.cell(i, 0).value)
    name = str(sh.cell(i, 1).value)
    currencies_d[name] = code

list_of_currencies = sorted(currencies_d.keys())


def cedi_to_oth(amount, curr):
	url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=GHS&to_currency=" + \
	    curr + "&apikey=SDX6VUX5ZH5RBERM"

	q = requests.get(url)
	json_d = q.json()
	json_d = json_d.values()
	json_d = json_d[0]
	rate = json_d["5. Exchange Rate"]
	rate = rate.encode("ascii", "replace")
	rate = float(rate)

	converted_amount = rate * float(amount)
	converted_amount = round(converted_amount, 2)

	return str(converted_amount)


@app.route('/')
def index():
  return render_template('index.html', list_of_currencies=list_of_currencies)


@app.route('/result', methods=['POST', 'GET'])
def res():
	if request.method == 'POST':
		value = request.form['value']
		currency_name = request.form['currency']
		currency = currencies_d[currency_name]

		fresult = cedi_to_oth(value, currency)
		return render_template('result.html', fresult=fresult, currency_name=currency_name)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
#    app.run(debug=True, port=33507)
