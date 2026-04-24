from flask import Flask, request, Response
import requests
from simpleeval import simple_eval

app = Flask(__name__)

@app.route('/')
def handle_query():
    airport = request.args.get('queryAirportTemp')
    if airport:
        try:
            headers = {'User-Agent': 'curl/7.64.1'}
            r = requests.get(f"https://wttr.in/{airport}?format=%t&m", headers=headers)
            temp_raw = r.text.replace('°C', '').replace('+', '').strip()
            temp_cleaned = "".join(c for c in temp_raw if c.isdigit() or c in ".-")
            
            return Response(str(float(temp_cleaned)), mimetype='application/json')
        except Exception as e:
            return f"Error: {str(e)}", 400
        
    stock = request.args.get('queryStockPrice')
    if stock:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            data = r.json()
            price = data['chart']['result'][0]['meta']['regularMarketPrice']
            return Response(str(float(price)), mimetype='application/json')
        except:
            return "Error fetching stock price", 400
        
    expr = request.args.get('queryEval')
    if expr:
        try:
            result = simple_eval(expr)
            return Response(str(float(result)), mimetype='application/json')
        except:
            return "Error in math expression", 400

    return "No valid query parameter", 400

if __name__ == '__main__':
    app.run()
