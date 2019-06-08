import sys
import os
# Ścieżka dla importu modułów
sys.path.append(os.getcwd()+'\\modules\\')
import database

# Ładuje dane z csv do bazy danych
# database.load_stock_data()

# Pobiera dane o walorach z internetu     
# database.download_data()

# Wypakowuje dane
# database.unzip_file()

# Inicjuje dane o dziennych zmianach w bazie danych 
# database.load_stocks_details()