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