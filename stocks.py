import sys
import os
# Ścieżka dla importu modułów
sys.path.append(os.getcwd()+'\\modules\\')
import database

# Ładuje dane z csv do bazy danych
# database.load_stock_data()

# stocks = database.get_data('stocks')
# for v in stocks:
#     print(v)
    
database.download_data()