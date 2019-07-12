import sys
import database
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import json


def get_stock_data(stock):
    """
    Zwraca wszytkie wartość z bazy danych dla danego waloru, konwertuje je na DataFrame i ustawia date jako index.
    Wartości są sortowane wg daty.
    Parameters
    ----------
    stock:String
        Nazwa waloru
    """
    df = pd.DataFrame(database.get_all_stock_data(stock), columns=[
                      'NAME', 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'])
    df.set_index('DATE', inplace=True)
    return df.sort_values(by=['DATE'])


def stock_dates_range(frame, start, end):
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
    dates = pd.date_range(start_date, end_date)
    new_df = pd.DataFrame(index=dates)
    new_df = new_df.join(df).dropna()
    return new_df


def stock_mean_volume(df):
    """
    Oblicza średnią wartość dla danej warości

    Parameters
    ----------
    df:DataFrame
    Dataframe z warościami do obliczeń

    Oblicza średni wolumen 
    """
    return df.mean(axis=0)


def draw_chart(df):
    """
    rysuje wykres 

    Parameters
    ----------
    df:DataFrame
    DataFrame z wartościami dla danego waloru 

    """
    trace = go.Candlestick(
        x=df.index,
        open=df['OPEN'],
        high=df['HIGH'],
        low=df['LOW'],
        close=df['CLOSE'],
        increasing=dict(line=dict(color='#1bbe02')),
        decreasing=dict(line=dict(color='#be0202'))
    )
    layout = go.Layout(
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        ),
        margin={'l': 75, 'r': 75, 't': 10, 'b': 25}
    )
    data = [trace]
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
