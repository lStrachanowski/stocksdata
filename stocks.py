import sys
import os
# Ścieżka dla importu modułów
sys.path.append(os.getcwd()+'\\modules\\')
import database
import csv
from flask import Flask
from flask import render_template, request
import requests
app = Flask(__name__)

@app.route('/' , methods=['GET', 'POST'])
def index():
    stock_list = database.get_data('stocks')
    # database.update_db()
    if request.method == 'POST':
        print(request.form.get('stock_fist_form')) 
        print(request.form.get('search_value'))
        
    return render_template('index.html', stock_list=list(stock_list))

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





