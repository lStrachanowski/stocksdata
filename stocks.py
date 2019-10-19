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
import matplotlib.pyplot as plt
import numpy as np
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

@app.route('/analyze', methods=['GET','POST'])
def analyze():
        analyze = analytics.analyze_volumes([90,30])
        return json.dumps([{"value": period} for period in analyze])

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

        sup_res = analytics.orders_supports_resistance(scraping.order_book(ticker, limited=False),stock)

        shareholders = scraping.get_shareholders(ticker)
        daily_returns = analytics.daily_retun(stock, 180)
        mean_vol_20 = analytics.volume_mean(stock, 180,20)
        mean_vol_65 = analytics.volume_mean(stock, 180,65)
        rolling_volume =  analytics.draw_mean_volume([mean_vol_20,mean_vol_65])
        return render_template('stocks.html', stock=stock, close_price = list(database.check_last_entry(stock))[0][5], daily_return = d_return,
        graphJSON=analytics.draw_chart(df,sup_res, 180),
        company_details = info,
        indicators = indicators,news = news,finance = financial_data, order_book = order_book, shareholders = shareholders, ticker = ticker, daily =  analytics.draw_daily_returns(daily_returns,90)
        , histogram = analytics.draw_daily_returns_histogram(daily_returns,90), mean_volume = rolling_volume)

@app.route('/<stock>/details', methods=['GET','POST'])
def stock_details(stock):
        df = analytics.get_stock_data(stock)
        t_min = df.tail().iloc[-2]['CLOSE']
        t = df.tail().iloc[-1]['CLOSE']
        d_return = round(((t/t_min)-1)*100,2)
        day_df = database.get_intraday_data(stock)
        last_entry = database.check_last_entry(stock)
        last_entry_date = int(str(list(last_entry)[0][1]).replace('-',''))
        volume_distribution = analytics.draw_volume_distribution(day_df[day_df.index == last_entry_date].groupby('CLOSE')['VOLUME'].sum())
        return render_template('details.html',stock=stock,close_price = list(database.check_last_entry(stock))[0][5], daily_return = d_return,volume_distribution =volume_distribution )

@app.route('/news' , methods=['GET','POST'])
def news():
        data = scraping.get_calendar()
        return render_template('news.html', news = data )

@app.route('/market', methods=['POST', 'GET'])
def market():
        shorts = scraping.short_sale()
        after_market = scraping.download_marketdata()
        return render_template('market.html', shorts=shorts, market = after_market)


@app.route('/bollsignals', methods=['POST','GET'])
def bollsignals():
        stock_list = database.get_data('stocks')
        up, down = analytics.bollinger_crossing(stock_list,65)
        return render_template('bollsignals.html', boll_up = up, boll_down = down )

@app.route('/sma/smacrossing', methods=['POST','GET'])
def smacrossing():
        results = []
        sma_15_results = []
        stock_list = database.get_data('stocks')
        for stock in stock_list:
                values = analytics.sma_crossing(stock[1],50,200)
                results.append(values)
                sma_15 = analytics.sma_price_crossing(stock[1],15)
                sma_15_results.append(sma_15)
        results = list(filter(None,results))
        sma_15_results = list(filter(None,sma_15_results))
        return render_template('sma.html', sma_crossing = results, sma_15=sma_15_results)


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




