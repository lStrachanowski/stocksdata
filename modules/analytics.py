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


def draw_chart(df, period=False):
    """
    rysuje wykres 

    Parameters
    ----------
    df:DataFrame
    DataFrame z wartościami dla danego waloru 

    Attributes
    ----------
    period : Integer, optional
        Zakres w dniach , na jaki ma zostać narysowany wykres
    """
    trace_candle = go.Candlestick(
        x=df[-period:].index,
        open=df['OPEN'][-period:],
        high=df['HIGH'][-period:],
        low=df['LOW'][-period:],
        close=df['CLOSE'][-period:],
        increasing=dict(line=dict(color='#1bbe02')),
        decreasing=dict(line=dict(color='#be0202')),
        name='Candle'
    )
    sma_200 = df['CLOSE'].rolling(200).mean()
    sma_50 = df['CLOSE'].rolling(50).mean()

    trace_sma200 = go.Scatter(
        x=df.index[-period:],
        y=sma_200[-period:],
        name='SMA 200',
        line=dict(
            color=('rgb(255, 155, 74)'),
            width=2,)
    )

    trace_sma50 = go.Scatter(
        x=df.index[-period:],
        y=sma_50[-period:],
        name='SMA 50',
        line=dict(
            color=('rgb(56, 148, 153)'),
            width=2,)
    )

    volume_bars = go.Bar(
        x=df.index[-period:],
        y=df['VOLUME'][-period:],
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=0.5),
        ),
        opacity=0.2,
        yaxis='y2',
        name='volume'
    )

    layout = go.Layout(
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        ),
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right'
        ),
        margin={'l': 75, 'r': 75, 't': 10, 'b': 25}
    )
    data = [trace_candle, trace_sma200, trace_sma50, volume_bars]
    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
