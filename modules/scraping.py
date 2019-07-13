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
            table_converted =list(table)
            company_details.append(table_converted[0])
            company_details.append(table_converted[2])
            company_details.append(table_converted[4])
            company_details.append(table_converted[6])
            for i in enumerate(table_converted[9]):
                company_details.append(i[1])
            for j in enumerate(table_converted[12]):
                company_details.append(j[1])
            company_details.append(table_converted[21])
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


