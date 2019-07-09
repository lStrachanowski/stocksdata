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

def stock_dates_range(frame, start,end):
    """
    Zwraca wartość z danego DataFrame , między dwoma podanymi datami.
    Parameters
    ----------
    frame:DataFrame
        DataFrame z wartościami dla danego waloru 
    start:String
        Początkowa data
    end:String
        Końcowa data
    """
    df = frame
    start_date = start
    end_date = end
    dates = pd.date_range(start_date,end_date)
    new_df = pd.DataFrame(index=dates)
    new_df = new_df.join(df).dropna()
    return new_df