import sys
import os
import requests
import zipfile
import datetime
from sqlalchemy import create_engine, MetaData, Table, Column,String,Numeric,Integer,Time,Date, select,exists, func, and_, text,Float,desc
sys.path.append(os.getcwd()+'\\modules\\')
import credentials 
# zawiera login i hasło do bazy danych 
import csv
engine = create_engine("postgresql://postgres:"+credentials.PASSWORD + "@localhost/" + credentials.DATABASE_NAME)
meta = MetaData()

# Towrzy tabele stocks
stocks = Table(
    "stocks", meta,
    Column("TICKER", String, primary_key=True),
    Column("NAME",String),
    Column("ISIN",String)
)

# Tworzy tabelę z podsumowaniem transakcji dnia
day_transactions = Table(
    'day_transactions', meta, 
    Column("NAME", String),
    Column("DATE", Date),
    Column("OPEN",Numeric),
    Column("HIGH",Numeric),
    Column("LOW",Numeric),
    Column("CLOSE",Numeric),
    Column("VOLUME",Float )
)

# Tworzy tabele z transakcjami w ciągu dnia
details_day_transactions = Table(
    'details_day_transactions', meta, 
    Column("NAME", String),
    Column("DATE", Date),
    Column("HOUR",Time),
    Column("OPEN",Numeric),
    Column("HIGH",Numeric),
    Column("LOW",Numeric),
    Column("CLOSE",Numeric),
    Column("VOLUME",Numeric )
)


# Inicjuje tabele w bazie danych
# meta.create_all(engine)


def table_operations(table_name, operation):
    """
     Usuwa / tworzy tabele z bazy danych 

    Parameters
    ----------
    table_name:String
        Nazwa tabeli w bazie danych 

    operation:String
        W zależności od opcji wykonywane są operacje na tabeli:
        - d 
          "drop" usuwa tabelę z bazy danych 
        - c
          "create" tworzy tabelę w bazie danych
    """
    if table_name == 'stocks':
        if operation == 'd':
            stocks.drop(engine)
        if operation == 'c':
            stocks.create(engine)
    elif table_name == 'daytransactions':
        if operation == 'd':
            day_transactions.drop(engine)
        if operation == 'c':
            day_transactions.create(engine)
    else:
        if operation == 'd':
            details_day_transactions.drop(engine)
        if operation == 'c':
            details_day_transactions.create(engine)
        
def load_stock_data(remove_old=False):
    """
    Metoda, która pobiera dane walorów z pliku csv i dodaje je do bazy danych
     Attributes
    ----------
    period : Boolean, optional
        Opcjonalne sprawdzanie i usówanie starych walorów z pliku csv, na podstawie , którego tworzone są wpisy w bazie danych. 
    """
    if remove_old:
        results = []
        full_data = []
        with open(os.getcwd()+'\\stock_tickers.csv' ,newline='', mode='r') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=';')
            for item in csv_data:
                results.append(item[0])
                full_data.append(item)
        with open (os.getcwd()+ '\\oldstocks.csv', newline='',mode='r') as old_csv:
            old_csv_data = csv.reader(old_csv, delimiter=';')
            for v in old_csv_data:
                try:
                    if(v[0][:-4] in results):
                        del results[results.index(v[0][:-4])] 
                except:
                    print(v)
        with open('stock_tickers.csv', mode='w',newline="") as c_f:
            ew = csv.writer(c_f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for val in full_data:
                if val[0] in results:
                    ew.writerow(val)          
               
    with open(os.getcwd()+'\\stock_tickers.csv' ,newline='', mode='r') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=';')
        stocks_data = []
        for row in csv_data:
            stocks_data.append( {"TICKER":row[1], "NAME":row[0],"ISIN":row[2]})
        conn = engine.connect()
        conn.execute(stocks.insert(), stocks_data)
        conn.close()

def get_all_stock_data(stock):
    """
    Pobiera wszystkie wartości o danego waloru z bazy danych
    Parameters:
    stock: String
        Nazwa waloru
    """
    selected = day_transactions.select().where(day_transactions.c.NAME == stock.upper())
    conn = engine.connect()
    data = conn.execute(selected)
    conn.close()
    return data
    
def get_data_from_db(from_date,to_date,stock_name):
    """
    Pobiera z bazy dane o walorze z podanego okresu
    
    Parameters
    ----------
    from_date:String
        Data , od której zacząć podbieranie danych o walorze

    to_date:String
        Data , do której zacząć podbieranie danych o walorze

    stock_name:String
        Nazwa waloru do wyszukania w bazie danych 
    """
    selected = day_transactions.select().where(and_(day_transactions.c.DATE >= from_date , day_transactions.c.DATE <= to_date, day_transactions.c.NAME == stock_name.upper())).order_by(day_transactions.c.DATE)
    conn = engine.connect()
    data = conn.execute(selected)
    conn.close()
    return data 

def check_last_entry(stock):
    """
    Sprawdza datę ostatniego wpisu w bazie danych 
    Parameters
    ----------
    stock:String
    Nazwa waloru
    """
    selected = day_transactions.select().where(day_transactions.c.NAME == stock).order_by(desc(day_transactions.c.DATE)).limit(1)
    conn = engine.connect()
    data = conn.execute(selected)
    conn.close()
    return data

def load_stocks_details():
    """
    Pobiera dane z plików i inicjuje je w bazie danych
    """
    directory = os.getcwd()+'\\data\\'
    for file in os.listdir(directory):
        print(file)
        with open(directory+file,newline='', mode="r" ) as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            stocks_data = []
            itercsv = iter(csv_data)
            next(itercsv)
            for row in itercsv:
                datetime_object = datetime.datetime.strptime(row[1],"%Y%m%d")
                name = row[0]
                stock_open = row[2]
                stock_high = row[3]
                stock_low = row[4]
                stock_close = row[5]
                stock_volume = row[6]
                stocks_data.append({"NAME":name,"DATE":datetime_object, "OPEN": float(stock_open),"HIGH": float(stock_high), "LOW": float(stock_low), "CLOSE": float(stock_close), "VOLUME": float(stock_volume)  })
            conn = engine.connect()
            conn.execute(day_transactions.insert(), stocks_data)
            conn.close()

def add_stock_data(stock):
    """
    Dodaje pozycje o walorze do bazy danych

    Parameters
    ----------
    stock:String
        Nazwa waloru
    """

    stocks_data = []
    datetime_object = datetime.datetime.strptime(stock[1],"%Y%m%d")
    name = stock[0]
    stock_open = stock[2]
    stock_high = stock[3]
    stock_low = stock[4]
    stock_close = stock[5]
    stock_volume = stock[6]
    stocks_data.append({"NAME":name,"DATE":datetime_object, "OPEN": float(stock_open),"HIGH": float(stock_high), "LOW": float(stock_low), "CLOSE": float(stock_close), "VOLUME": float(stock_volume)  })
    conn = engine.connect()
    conn.execute(day_transactions.insert(), stocks_data)
    conn.close()

def get_stock_marks(stock,isin=False,ticker=False):
    """
    Zwraca ISIN lub TICKER dla danego waloru

    Attributes
    ----------
    isin : Boolean, optional 
        Zwraca ISIN waloru 
    
    ticker: Boolean, optinal
        Zwraca TICKER dla danego waloru

    Parameters
    ----------
    stock:String
        Nazwa waloru 
    """
    conn = engine.connect()
    result = stocks.select().where(stocks.c.NAME == stock.upper())
    data = conn.execute(result)
    conn.close()
    if isin:
        return list(data)[0][2]
    if ticker:
        return list(data)[0][0]

def get_data(value):
    """
    Pobiera wartości z bazy danych 

    Parameters
    ----------
    value:String
        W zależności od wartości pobiera dane z wybranej tabeli
    """

    if value == 'stocks':
        selected = stocks.select()
        conn = engine.connect()
        results = conn.execute(selected)
        conn.close()
        return results
    elif value =='day_transactions':
        selected = day_transactions.select()
        conn = engine.connect()
        results = conn.execute(selected)
        conn.close()
        return results
    elif value =='details_day_transactions':
        selected = details_day_transactions.select()
        conn = engine.connect()
        results = conn.execute(selected)
        conn.close()
        return results

def download_data():
    """
    Pobiera dane end of day ze strony BOŚ
    """
    url = "http://bossa.pl/pub/metastock/mstock/mstall.zip"
    url_newconnect = "http://bossa.pl/pub/newconnect/mstock/mstncn.zip"
    path = os.getcwd()+'\\data\\'
    try:
        print("Downloading GPW data.")
        r = requests.get(url)
        with open(path + 'mstall.zip' , "wb") as code:
            code.write(r.content)
        print("Downloading GPW data ended.")
    except requests.exceptions.RequestException as e:
        print("Something went wrong with dowloading GPW data.")
        print(e)
    try:
        print("Downloading NewConnect data.")
        r = requests.get(url_newconnect)
        with open(path + 'mstncn.zip' , "wb") as code:
            code.write(r.content)
        print("Downloading NewConnect data ended.")
    except requests.exceptions.RequestException as e:
        print("Something went wrong with dowloading NewConnect data.")
        print(e)

def unzip_file(directory, file_list):
    """
    Wypakowuje dane z pliku zip I usuwa zbędne pliki 

    Parameters
    ----------
    directory:String
        Ścieżka do lokalizacji

    file_list:List
        Lista z nazwami plików do rozpakowania
    """
    try:
        for item in file_list:
            print('Unzipping ' + item + ' file.')
            with zipfile.ZipFile(directory + item) as myzip:
                myzip.extractall(directory)
            print(item + ' files unziped.')
            if os.path.isfile(directory + item):
                os.remove(directory + item ) 
    except:
        print("Something went wrong with file unzipping")

def delete_old_files():
    """
    Usuwa pliki ze starymi akcjami 
    """
    directory = os.getcwd()+'\\data\\'
    print('Start to delete old files')
    with open('oldstocks.csv', newline='') as file:
        reader = csv.reader(file, delimiter=' ')
        for item in list(reader)[:-1]:
            file_path = directory + item[0]
            if os.path.isfile(file_path):
                os.remove(file_path)
    print('Old files deleted')
    print('Start to delete old files')
    for file in os.listdir(directory):
        conn = engine.connect()
        check = exists(select([stocks]).where(stocks.c.NAME == file[:-4])).select()
        pr = conn.execute(check)
        conn.close()
        if pr.first()[0] == False:
            if os.path.isfile(directory + file):
                os.remove(directory + file)
    print('Old files deleted')    

def download_week():
    """
    Pobiera aktualne dane ze strony bossa.pl
    """
    url = "https://info.bossa.pl/pub/metastock/mstock/sesjaall/few_last.zip"
    path = os.getcwd()+'\\temp\\'
    try:
        r = requests.get(url)
        with open(path + "gpw.zip", "wb" ) as code:
            code.write(r.content)
    except requests.exceptions.RequestException as e:
        print("Something went wrong with dowloading GPW data.")
        print(e)
    
def check_stock(stock):
    """
    Sprawdza czy plik z danym walorem jest w bazie danych

    Parameters
    ----------
    stock:String
        Nazwa waloru 
    """
    conn = engine.connect()
    check = exists(select([stocks]).where(stocks.c.NAME == stock)).select()
    pr = conn.execute(check)
    conn.close()
    return pr.first()[0]

def update_db(get_days=False, number_of_days=False): 
    """
    Aktualizuje bazę danych

    Attributes
    ----------
    get_days : Boolean, optional 
        zwraca True albo False w zależności czy różnica między ostatnią datą w bazie danych a obecną datą jest większa od zera

    number_of_days : Boolean, optional
        pobiera różnicę w datach ostatniej wartości w bazie danych a obecną datą 
    """
    today_date = datetime.date.today()
    last_date = list(check_last_entry('WIG20'))[0][1]
    diff = today_date - last_date
    now = datetime.datetime.now()
    if number_of_days:
        if diff.days <= 2 and last_date.weekday() == 4 and today_date.weekday() > 4:
            return 0
        else:
            return diff.days

    if get_days:
        if diff.days > 0 and diff.days < 7:
            if last_date.weekday() == 4 and today_date.weekday() > 4:
                return False
            else:
                if diff.days > 0 and now.hour < 19:
                    return False
                else:
                    return True
        else:
            return True

    if diff.days < 7:
        download_week()
        unzip_file(os.getcwd()+'\\temp\\',['gpw.zip'])
        file_list = os.listdir(os.getcwd()+'\\temp\\')
        for file in file_list:
            s = file.split(".")[0]
            if s[0] == '2':
                file_time = datetime.datetime.strptime(s, '%Y%m%d' )
                db_last_time = datetime.datetime(last_date.year, last_date.month, last_date.day)
                t_diff = file_time - db_last_time
                if t_diff.days > 0 :
                    print("do dodania " + file)
                    with open(os.getcwd()+'\\temp\\'+file, newline='') as prn_file:
                        reader = csv.reader(prn_file, delimiter=',')
                        for r in reader:
                            if check_stock(r[0]):
                                add_stock_data(r)
        print('Baza aktualna')
    else:
        print('Odświeżanie bazy danych')
        table_operations('daytransactions','d')
        table_operations('daytransactions','c')
        download_data()
        unzip_file(os.getcwd()+'\\data\\',['mstall.zip','mstncn.zip'])
        delete_old_files()
        load_stocks_details()
        print('Baza aktualna')

def search_value(value):
    """
    Szuka w bazie danych nazwy waloru zawierającej parametr value

    Parameters
    ----------
    value:String
        watość do wyszukania w bazie danych 
    """
    conn = engine.connect()
    result = stocks.select().where(stocks.c.NAME.like('{}%'.format(value.upper())))
    data = conn.execute(result)
    conn.close()
    return data

