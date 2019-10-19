import sys
import database
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import json
import decimal
from datetime import date
import time
from decimal import Decimal


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
    Oblicza średnią dla danego zakresu warości

    Parameters
    ----------
    df:DataFrame
    Dataframe z warościami do obliczeń

    """
    return df.mean(axis=0)

def draw_chart(df, sup_res, period=False):
    """
    rysuje wykres 

    Parameters
    ----------
    df:DataFrame
    DataFrame z wartościami dla danego waloru 

    sup_res:List
    Lista z cenami, na których jest najwięcej zleceń kupna i sprzedaży w arkuszu zleceń

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
        name='Candle'
    )

    sma_200 = df['CLOSE'].rolling(200).mean()
    sma_50 = df['CLOSE'].rolling(50).mean()
    sma_15 = df['CLOSE'].rolling(15).mean()

    # Sma 200
    trace_sma200 = go.Scatter(
        x=df.index[-period:],
        y=sma_200[-period:],
        name='SMA 200',
        line=dict(
            color=('rgb(255, 155, 74)'),
            width=2,),
        hoverinfo='none'
    )

    # Sma 50
    trace_sma50 = go.Scatter(
        x=df.index[-period:],
        y=sma_50[-period:],
        name='SMA 50',
        line=dict(
            color=('rgb(56, 148, 153)'),
            width=2,),
        hoverinfo='none'
    )

    trace_sma15 = go.Scatter(
        x=df.index[-period:],
        y=sma_15[-period:],
        name='SMA 15',
        line=dict(
            color=('rgb(68, 21, 196)'),
            width=2,),
        hoverinfo='none'
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
            width=2,),
        hoverinfo='none'
    )

    boll_65_up = go.Scatter(
        x=df.index[-period:],
        y=boll_up[-period:],
        name='Bollinger up',
        line=dict(
            color=('rgba(209, 181, 185, 0.5)'),
            width=2,),
        hoverinfo='none'
    )
    data = []
    
    if len(sup_res[0]) > 0:
        for val in sup_res[0]:
            data.append( {
            'type': 'line',
            'x0': 0,
            'y0': float(val),
            'x1': 180,
            'y1': float(val),
            'line': {
                'color': 'rgba(128, 112, 110,0.25)',
                'width': 2
            }
        })
    if len(sup_res[1]) > 0:
        for val in sup_res[1]:
            data.append( {
            'type': 'line',
            'x0': 0,
            'y0': float(val),
            'x1': 180,
            'y1': float(val),
            'line': {
                'color': 'rgba(26, 158, 12,0.25)',
                'width': 2
            }
        })

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
        margin={'l': 75, 'r': 75, 't': 10, 'b': 80},
        shapes= data
    )
    
    data = [trace_candle, trace_sma200, trace_sma50,trace_sma15,
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
        margin={'l': 75, 'r': 75, 't': 10, 'b': 80},
        shapes=[]
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

    period : Integer
        Zakres w dniach , na jaki ma zostać narysowany wykres
    """
    
    x = df[-period:]
    layout = go.Layout(
         margin={'l': 75, 'r': 75, 't': 10, 'b': 30},
         width=600,
         height=350,
         xaxis=dict(
         tick0=0,
         dtick=2.0,
        ),bargap=0.1
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

def volume_mean(stock, days, period):
    """
    Zwraca średnią kroczącą wolumenu. 
    Parameters
    ----------
    stock:String
        Nazwa waloru
    days:Integer
        Średnia krocząca z ppodanej liczby dni
    period:Integer
        Zakres dni, dla których ma zostać obliczona średnia krocząca.
    """
    data = get_stock_data(stock)
    mean_volume = data['VOLUME'].rolling(period).mean().dropna()[-days:]
    return mean_volume

def draw_mean_volume(lista):
    """
    Rysuje wykres średniej kroczącej wolumenu. 
    Parameters
    ----------
    lista:List
    Lista z DataFrames dla poszczególnych zakresów czasowych dla danego waloru 

    """

    x_20 = list(lista[0].index)
    y_20 = list(lista[0])
    x_65 = list(lista[1].index)
    y_65 = list(lista[1])
    layout = go.Layout(
         margin={'l': 75, 'r': 75, 't': 10, 'b': 30},
         width=700,
         height=450
    )
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Scatter(x = x_20, y = y_20, name='20 dni'))
    fig.add_trace(go.Scatter(x = x_65, y = y_65, name='65 dni'))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def draw_volume_distribution(df):
    """
    Rysuje wykres dziennego rozkładu wolumenu
    Parameters
    ----------
    df:DataFrame
    Dataframe z volumenami dla danego poziomu cenowego
    """
    x = df.index
    y = df
    layout = go.Layout(
        xaxis=dict(
            type="category",
            showticklabels=False
        ),
         width=750,
         height=500,
         margin={'l': 75, 'r': 75, 't': 10, 'b': 30}
    )
    fig = go.Figure([go.Bar(x=x, y=y)], layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def analyze_volumes(period):
    """
    Wyszukuje skoków wolumenu u stosunku do średniej z danego okresu
        Parameters
    ----------
    period:List
        Lista z liczba dni, dla których wyliczamy średnią.
    """
    start_time = time.time()
    stocks_list = database.get_data('stocks')
    df  = pd.DataFrame(stocks_list,columns=['TICKER', 'NAME', 'ISIN'] )
    df_results = pd.DataFrame(columns=['NAME','PERIOD','CHANGE','CLOSE','DAILY'])
    for name in df['NAME']:
        try:
            data = get_stock_data(name)
            current_volume = data.iloc[-1]['VOLUME']
            vol_value = float(data.iloc[-1]['CLOSE']) * current_volume 
            if vol_value > 80000 :
                for value in period:
                    mean = stock_mean_volume(data[-value:]['VOLUME'])
                    current_volume = data[-value:].iloc[-1]['VOLUME']
                    vol_percent = round((((current_volume/mean)-1)*100),2)
                    close_price = list(database.check_last_entry(name))[0][5]

                    t_min = data.tail().iloc[-2]['CLOSE']
                    t = data.tail().iloc[-1]['CLOSE']
                    d_return = round(((t/t_min)-1)*100,2)

                    df_results = df_results.append({'NAME':name,'PERIOD':value,'CHANGE':vol_percent,'CLOSE':float(close_price),'DAILY':float(d_return)},ignore_index=True)
                    print(name, value)
            else:
                print("Za mały obrót", name)
        except Exception as e:
            print(name, " Error", e)
    result_table = []
    for p_value in period:
        r_item = df_results[df_results['PERIOD'].isin([p_value])].sort_values(by =['CHANGE'], ascending=False)
        result_table.append(r_item.values.tolist())
    print("Executed in : {} seconds".format(time.time() - start_time) )

    return result_table
    
def reactivnes():
    """
    Oblicza Alfe i betę dla waloru z WIG20 względem zmiany WIG20
    """
    today = date.today()
    stock_data = get_stock_data('PZU')
    stock_data.sort_values(by=['DATE'])

    index_data = database.get_data_from_db(stock_data.index[0],today,'WIG20')
    index_df = pd.DataFrame(index_data, columns=['NAME', 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'])
    index_df.set_index('DATE', inplace=True)

    stock_daily_return = daily_retun('PZU', 250)
    index_daily_return = daily_retun('WIG20', 250)
    beta_stock, alpha_stock = np.polyfit(index_daily_return, stock_daily_return ,1 )

    print ("BETA = {}, ALPHA = {}".format(beta_stock, alpha_stock))

def bollinger_crossing(df,period):
    """
    Znajduje walory , których aktualny kurs przebił wstęgę bollingera od góry bądź dołu.
    Parameters
    ----------
    df:DataFrame
    DataFrame z nazwami walorów

    period:Integer
    Liczba dni, dla których wyliczamy średnią.
    """
    results_up = []
    results_down = []
    print("Analyzing ...")
    for value in df:
        print(value['NAME'])
        try:
            stock_df = get_stock_data(value['NAME'])
            sma = stock_df['CLOSE'].rolling(period).mean()[-1]
            sma_std = stock_df['CLOSE'].rolling(period).std()[-1]
            boll_up = sma + (2 * sma_std)
            boll_down = sma - (2 * sma_std)
            if stock_df['CLOSE'][-1] >= boll_up:
                results_up.append(stock_df['NAME'][-1])
            if stock_df['CLOSE'][-1] <= boll_down:
                results_down.append(stock_df['NAME'][-1])
        except Exception as e:
            print(value['NAME'], e)
    print("Analyzing ended...")
    return (results_up,results_down)
    
def sma_crossing(stock, first_sma,second_sma):
    """
    Znajduje walory , których sma się przecinają.
    Parameters
    ----------
    stock:String
    Nazwa waloru

    first_sma:Integer
    Pierwsza sma

    second_sma:Integer
    Druga sma
    """
    try:
        stock_data = get_stock_data(stock)
        second_sma_values = stock_data['CLOSE'].rolling(second_sma).mean().dropna()
        first_sma_values = stock_data['CLOSE'].rolling(first_sma).mean().dropna()[-len( second_sma_values):]
        first_sma_values_moved = first_sma_values.shift(1).dropna()
        second_sma_values_moved = second_sma_values.shift(1).dropna()
        res =  stock_data.where( ((first_sma_values < second_sma_values) & (first_sma_values_moved >= second_sma_values_moved)) |
        ((first_sma_values > second_sma_values) & (first_sma_values_moved <= second_sma_values_moved))).dropna()
        difference = date.today() - list(res.index)[-1]
        print(stock,difference.days)
        if difference.days < 7 :
            return [stock,difference.days]
    except Exception as e:
        print(stock, e)

def sma_price_crossing(stock, sma):
    """
    Znajduje walory , których sma przecina cenę zamkniecia. 
    Parameters
    ----------
    stock:String
    Nazwa waloru

    sma:Integer
    Sma
    """
    try:
        stock_data = get_stock_data(stock)
        turnover = stock_data.iloc[-1]['VOLUME'] * float(stock_data.iloc[-1]['CLOSE'])
        if turnover > 80000 :
            print(turnover)
            sma_values = stock_data['CLOSE'].rolling(sma).mean().dropna()
            sma_values_moved = sma_values.shift(1).dropna()
            curr_stock_data = stock_data[-len(sma_values):]['CLOSE']
            all_stock_moved = curr_stock_data.shift(1).dropna()
            res =  stock_data.where( ((sma_values < curr_stock_data) & (sma_values_moved >= all_stock_moved)) |
            ((sma_values > curr_stock_data) & (sma_values_moved <= all_stock_moved))).dropna()
            difference = date.today() - list(res.index)[-1]
            print(stock,difference.days)
            if difference.days < 3:
                return [stock, difference.days]
    except Exception as e:
        print(stock,e)

def orders_supports_resistance(data, stock):
    """
    Zwraca pięć cen , na których jest najwięcej zleceń kupna i sprzedaży w arkuszu zleceń
    Parameters
    ----------
    data:List
    Lista z danymi z arkusza zleceń
    stock:String
    Nazwa waloru
    """
    try:
        current_close = get_stock_data(stock)['CLOSE'][-1]
        buy, sell = data[0] , data[1]
        for i in range(len(buy)-1) :
            temp = Decimal(buy[i][2].replace(',','').replace(',','.'))
            buy[i][2] = temp
        b_array = list(filter(lambda x: float(x[0]) > (float(current_close) - ( 0.5 * float(current_close))), buy[:-1]))
        buy_array = np.array(b_array)[:-1]
            
        for i in range(len(sell)-1) :
            temp = Decimal(sell[i][2].replace(',','').replace(',','.'))
            sell[i][2] = temp
        s_array = list(filter(lambda x: float(x[0]) <  (float(current_close) + (0.5 * float(current_close))), sell[:-1]))
        sell_array = np.array(s_array)[:-1]
        return[buy_array[buy_array[:,2].argsort()][-5:][:,0].tolist(), sell_array[sell_array[:,2].argsort()][-5:][:,0].tolist()]
    except Exception as e:
        print(e)
        return [[],[]]
   





  