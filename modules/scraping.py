import requests
from bs4 import BeautifulSoup

def company_info(stock_ticker):
    """
    Pobiera informację o firmie ze strony stooq.pl
    Parameters
    ----------
    stock_ticker:String
        Ticker dla danego waloru.
    """
    base_url = r'https://stooq.pl/q/p/?s='
    if stock_ticker:
        page = requests.get(base_url+stock_ticker)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            full_company_name = soup.find('font', id='f14')
            table = soup.find('font', id='f13')
            company_details = []
            company_details.append(full_company_name.getText())
            for v in table:
                if len(v) > 1:
                    company_details.append(v)
            del company_details[-3:-1]
            links = table.find_all('a')
            for l in links[:2]:
                company_details.insert(-1,l.getText())
            return company_details

def company_indicators(stock_ticker):
    """
    Pobiera dane o wskaźnikach ze stooq
    Parameters
    ----------
    stock_ticker:String
        Ticker dla danego waloru.
    """
    base_url = r'https://stooq.pl/q/g/?s='
    if stock_ticker:
        page = requests.get(base_url+stock_ticker)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find_all('tr', id='f13')
            company_data = []
            for tab in table:
                td = tab.find_all('td')
                temp = []
                for i in td:
                    temp.append(i.getText())
                company_data.append(temp)
            cz = soup.find_all('table', id='t1')
            cwk_val = cz[1].find_all('td', id='f13')
            cz_val = cz[0].find_all('td', id='f13')
            if cwk_val:
                company_data.append(['C/WK',cwk_val[-1].getText()])
            else:
                company_data.append(['C/WK','N.A'])
            if cz_val:
                company_data.append(['C/Z',cz_val[0].getText()])
            else:
                company_data.append(['C/Z','N.A'])
            return company_data

def get_news(isin):
    """
    Pobiera komunikaty o danej spółce
    Parameters
    ----------
    isin:String
        Isin dla danego waloru.
    """
    base_url = r'https://www.money.pl/gielda/spolki-gpw/'
    if isin:
        page = requests.get(base_url+isin+',emitent,1.html')
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find_all('tr', {"class":'npeb8d-3'})
            news = []
            for val in table:
                td = val.find_all('td')
                data = []
                for v in td:
                    data.append(v.getText())
                    if v.find('a'):
                        link = r'https://www.money.pl' + v.find('a')['href']
                        data.append(link)
                news.append(data)
            return news[1:10:]

def get_financial_data(isin):
    """
    Pobiera dane o finansach danej społki
    Parameters
    ----------
    isin:String
        Isin dla danego waloru.
    """
    base_url = r'https://www.money.pl/gielda/spolki-gpw/'
    if isin:
        page = requests.get(base_url+isin+',finanse.html')
        if page.status_code == 200:
            soup = BeautifulSoup(page.content , 'html.parser',from_encoding="utf-8")
            table = soup.find_all(class_='fkmtpn-1')
            financial_years = []
            financial_data = []
            for item in table:
                data_table = item.find_all('tr', {"class":'fkmtpn-2'})
                all_data_table = []
                for val in data_table:
                    financial_data_item = []
                    td_head = val.find('td', {"class":'fkmtpn-5'})
                    td_values = val.find_all('td',{"class":'fkmtpn-6'})
                    td_years = val.find_all('td',{"class":'fkmtpn-4'})
                    for year in td_years:
                        financial_years.append(year.getText())
                    if td_head:
                        financial_data_item.append(td_head.getText())
                        if td_values:
                            temp_val = []
                            for item in td_values:
                                text = item.getText()
                                temp_val.append(text.replace(u'\xa0', ' '))
                            financial_data_item.append(temp_val)
                    all_data_table.append(financial_data_item)
                financial_data.append(all_data_table)
            return financial_years, financial_data


def order_book(ticker):
    """
    Pobiera dziesięć zleceń kupna i sprzedaży na podstawie tickera danych akcji 
    Parameters
    ----------
    ticker:String
        Ticker dla danego waloru.
    """
    base_url = r'https://gragieldowa.pl/spolka_arkusz_zl/spolka/'
    if ticker:
        page = requests.get(base_url+ticker)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find_all('tr')
            headers = []
            buy = []
            sell = []
            for i in range(4,len(table)-29):
                if table[i].find('th'):
                    headers.append(i)
            if headers:
                for val_buy in range(headers[0]+1,headers[1]):
                    buy_row_member = []
                    buy_row_member.append(table[val_buy].find('td').string)
                    sibling = (table[val_buy].find('td').next_siblings)
                    for s in sibling:
                        buy_row_member.append(s.string)
                    buy.append(buy_row_member)
                for val_sell in range(headers[1]+1,len(table)-29):
                    sell_row_member = []
                    sell_row_member.append(table[val_sell].find('td').string)
                    sibling = (table[val_sell].find('td').next_siblings)
                    for s in sibling:
                        sell_row_member.append(s.string)
                    sell.append(sell_row_member)  
                if len(buy) < 11:
                    buy = buy[:len(buy)-1]
                else:
                    buy = buy[0:10]
                if len(sell) < 11:
                    sell = sell[:len(sell)-1]
                else:
                    sell = sell[0:10]
                return (buy, sell)
            else:
                return ([0], [0])
        else:
            print('something went wrong with book order scrapping')


def get_shareholders(stock_ticker):
    """
    Pobiera dane o akcjonariacie
    Parameters
    ----------
    stock_ticker:String
        Ticker dla danego waloru.
    """
    base_url = r'https://stooq.pl/q/h/?s='
    if stock_ticker:
        page = requests.get(base_url+stock_ticker)
        rows_data = []
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find_all('table',class_="fth1")
            rows = table[0].find_all('tr',id='r')
            for v in rows:
                row_values = []
                for item in v.findChildren('td'):
                    row_values.append(item.getText())
                rows_data.append(row_values)
        return rows_data