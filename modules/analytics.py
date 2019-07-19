import sys
import database
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import json
import decimal


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
    # Wykres świecowy
    trace_candle = go.Candlestick(
        x=df[-period:].index,
        open=df['OPEN'][-period:],
        high=df['HIGH'][-period:],
        low=df['LOW'][-period:],
        close=df['CLOSE'][-period:],
        increasing=dict(line=dict(color='#1bbe02')),
        decreasing=dict(line=dict(color='#be0202')),
        name='Candle',
        hoverinfo='none'
    )

    sma_200 = df['CLOSE'].rolling(200).mean()
    sma_50 = df['CLOSE'].rolling(50).mean()

    # Sma 200
    trace_sma200 = go.Scatter(
        x=df.index[-period:],
        y=sma_200[-period:],
        name='SMA 200',
        line=dict(
            color=('rgb(255, 155, 74)'),
            width=2,)
    )

    # Sma 50
    trace_sma50 = go.Scatter(
        x=df.index[-period:],
        y=sma_50[-period:],
        name='SMA 50',
        line=dict(
            color=('rgb(56, 148, 153)'),
            width=2,)
    )

    # Volumen
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

    # Bollinger bands
    sma_65 = df['CLOSE'].rolling(65).mean()
    sma_65_std = df['CLOSE'].rolling(65).std()
    boll_up = sma_65 + (2 * sma_65_std)
    boll_down = sma_65 - (2 * sma_65_std)

    boll_65 = go.Scatter(
        x=df.index[-period:],
        y=sma_65[-period:],
        name='SMA 65',
        line=dict(
            color=('rgba(209, 181, 185, 0.5)'),
            width=2,),
        hoverinfo='none'
    )

    boll_65_down = go.Scatter(
        x=df.index[-period:],
        y=boll_down[-period:],
        name='Bollinger down',
        line=dict(
            color=('rgba(209, 181, 185, 0.5)'),
            width=2,)
    )

    boll_65_up = go.Scatter(
        x=df.index[-period:],
        y=boll_up[-period:],
        name='Bollinger up',
        line=dict(
            color=('rgba(209, 181, 185, 0.5)'),
            width=2,)
    )

    layout = go.Layout(
        xaxis=dict(
            rangeslider=dict(
                visible=False
            ),
            type="category"
        ),
        yaxis=dict(
            title='Price',
            side='left'
        ),
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right'
        ),
        margin={'l': 75, 'r': 75, 't': 10, 'b': 80}
    )
    data = [trace_candle, trace_sma200, trace_sma50,
            volume_bars, boll_65, boll_65_down, boll_65_up]
    fig = go.Figure(data=data, layout=layout)
    layout = go.Layout(
        xaxis=dict(
            rangeslider=dict(
                visible=False
            ),
            type="category"
        ),
        yaxis=dict(
            title='Price',
            side='left'
        ),
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right'
        ),
        margin={'l': 75, 'r': 75, 't': 10, 'b': 80}
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def draw_daily_returns(df, period):
    """
    Rysuje wykres dziennych stop zwrotu

    Parameters
    ----------
    df:DataFrame
    DataFrame z wartościami dla danego waloru 

    Attributes
    ----------
    period : Integer
        Zakres w dniach , na jaki ma zostać narysowany wykres
    """
    x = df.index[-period:]
    y = df[-period:]
    layout = go.Layout(
        xaxis=dict(
            type="category",
            showticklabels=False
        ),
         width=600,
         height=350,
         margin={'l': 75, 'r': 75, 't': 10, 'b': 30}
    )
    fig = go.Figure([go.Bar(x=x, y=y)], layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def draw_daily_returns_histogram(df, period):
    """
    Rysuje histogram dziennych stop zwrotu

    Parameters
    ----------
    df:DataFrame
    DataFrame z wartościami dla danego waloru 

    Attributes
    ----------
    period : Integer
        Zakres w dniach , na jaki ma zostać narysowany wykres
    """
    
    x = df[-period:]
    layout = go.Layout(
         margin={'l': 75, 'r': 75, 't': 10, 'b': 30},
         width=600,
         height=350
    )
    fig = go.Figure(data=[go.Histogram(x=x)], layout = layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON



def daily_retun(stock, days):
    """
    Zwraca dzienne zmiany waloru dla podanego okresu
    Parameters
    ----------
    stock:String
        Nazwa waloru
    days:Integer
        Liczba dni
    """
    data = get_stock_data(stock)[-days:]
    t_min = data.shift()
    result = (data['CLOSE']/t_min['CLOSE'] - 1) * 100
    result.iloc[0] = 0
    return result.astype('float').round(2)
