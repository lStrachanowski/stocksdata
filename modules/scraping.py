import requests
from bs4 import BeautifulSoup

def company_info(stock_ticker):
    """
    Ppobiera informację o firmie ze strony stooq.pl
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