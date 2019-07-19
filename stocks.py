import sys
import os
# Ścieżka dla importu modułów
sys.path.append(os.getcwd()+'\\modules\\')
import database
import analytics
import scraping
import csv
import json
from flask import Flask
from flask import render_template, request,redirect, url_for, jsonify
import requests
app = Flask(__name__)

stock_list = []

@app.route('/' , methods=['GET', 'POST'])
def index():
    stock_list = database.get_data('stocks')
    if request.method == 'POST':
        selected_result = request.form.get('stock_list_form')
        return redirect(url_for('stock', stock = selected_result))
    return render_template('index.html', stock_list = list(stock_list), update = database.update_db(get_days=True), days_counter = database.update_db(number_of_days=True) )
 
@app.route('/search' , methods=['GET', 'POST'])        
def search():
    if request.method == 'POST':
        search_results = request.form.get('search_value')
        if search_results:
                stock_list = database.search_value(search_results)
                return json.dumps([{"name": val[1]} for val in stock_list])
        else:
                return json.dumps([{"error": False}])

        
@app.route('/update', methods=['GET','POST'])
def update():
        database.update_db()
        return "updated"

@app.route('/<stock>', methods = ['GET','POST'])
def stock(stock):
        df = analytics.get_stock_data(stock)
        t_min = df.tail().iloc[-2]['CLOSE']
        t = df.tail().iloc[-1]['CLOSE']
        d_return = round(((t/t_min)-1)*100,2)
        ticker = database.get_stock_marks(stock, ticker=True)
        isin = database.get_stock_marks(stock, isin=True)
        info = scraping.company_info(ticker)
        indicators = scraping.company_indicators(ticker)
        news = scraping.get_news(isin)
        financial_data = scraping.get_financial_data(isin)
        order_book = scraping.order_book(ticker)
        shareholders = scraping.get_shareholders(ticker)
        daily_returns = analytics.daily_retun(stock, 180)
        mean_vol_20 = analytics.volume_mean(stock, 180,20)
        mean_vol_65 = analytics.volume_mean(stock, 180,65)

        rolling_volume =  analytics.draw_mean_volume([mean_vol_20,mean_vol_65])
        return render_template('stocks.html', stock=stock, close_price = list(database.check_last_entry(stock))[0][5], daily_return = d_return,
        graphJSON=analytics.draw_chart(df, 180),
        company_details = info,
        indicators = indicators,news = news,finance = financial_data, order_book = order_book, shareholders = shareholders, ticker = ticker, daily =  analytics.draw_daily_returns(daily_returns,90)
        , histogram = analytics.draw_daily_returns_histogram(daily_returns,90), mean_volume = rolling_volume)



# database.table_operations('stocks','c')

# Laduje dane z csv do bazy danych
# database.load_stock_data()

# Pobiera dane o walorach z internetu     
# database.download_data()

# Wypakowuje dane
# database.unzip_file(os.getcwd()+'\\data\\',['mstall.zip','mstncn.zip'])

#Kasuje niepotrzebne pliki
# database.delete_old_files()

# Inicjuje dane o dziennych zmianach w bazie danych 
# database.load_stocks_details()




