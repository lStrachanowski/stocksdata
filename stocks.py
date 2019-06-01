import sys
import os
# Ścieżka dla importu modułów
sys.path.append(os.getcwd()+'\\modules\\')
import database

# database.load_stock_data()

stocks = list(database.get_data('stocks'))
for v in stocks:
    print(v)
    
