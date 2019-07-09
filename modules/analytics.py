import sys
import database
import pandas as pd


def get_stock_data(stock):
    """
    Zwraca wszytkie wartość z bazy danych dla danego waloru, konwertuje je na DataFrame i ustawia date jako index.
    Wartości są sortowane wg daty.
    Parameters
    ----------
    stock:String
        Nazwa waloru
    """
    df = pd.DataFrame(database.get_all_stock_data(stock), columns=['NAME','DATE','OPEN','HIGH','LOW','CLOSE','VOLUME'])
    df.set_index('DATE', inplace = True)
    return df.sort_values(by=['DATE'])

