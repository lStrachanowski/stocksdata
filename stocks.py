import sys
import os
# Ścieżka dla importu modułów
sys.path.append(os.getcwd()+'\\modules\\')
import database
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
        print(list(database.check_last_entry(stock))[0])
        return render_template('stocks.html', stock=stock, close_price = list(database.check_last_entry(stock))[0][5] )

# Ładuje dane z csv do bazy danych
# database.load_stock_data()

# Pobiera dane o walorach z internetu     
# database.download_data()

# Wypakowuje dane
# database.unzip_file(os.getcwd()+'\\data\\',['mstall.zip','mstncn.zip'])

#Kasuje niepotrzebne pliki
# database.delete_old_files()

# Inicjuje dane o dziennych zmianach w bazie danych 
# database.load_stocks_details()


# res = database.get_data_from_db('20180501','20190603','11bit')
# for r in res:
#     print(r)





