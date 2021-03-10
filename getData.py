import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import requests
from bs4 import BeautifulSoup
import pytz
import json

# Connect to database
cred = credentials.Certificate('credentials.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

tz = pytz.timezone('Asia/Kolkata')


def get_sensex():
    ''' The function scraps yahoo finance website every minute and update the database values '''
    try:
        URL = "https://finance.yahoo.com/quote/%5EBSESN?p=^BSESN&.tsrc=fin-srch"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        # sensex = soup.find('span', attrs = {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})
        div = soup.find('div', attrs={'class': 'D(ib) Mend(20px)'})
        div = div.findAll('span')

        sensex_value = str(div[0].text)

        change = str(div[1].text).split(' ')
        sensex_change = change[0]
        sensex_pchange = change[1]

        sensex_timestamp = str(div[2].text)

        change_ispositive = None
        pchange_ispositive = None
        if(sensex_change[0] == '+'):
            change_ispositive = True
        else:
            change_ispositive = False

        if(sensex_pchange[1] == '+'):
            pchange_ispositive = True
        else:
            pchange_ispositive = False

        data = {
            "sensex_value": sensex_value,
            "change": sensex_change,
            "pchange": sensex_pchange,
            "change_ispositive": change_ispositive,
            "pchange_ispositive": pchange_ispositive,
            "lastUpdated": datetime.datetime.now(tz=tz)
        }

        db.collection(u'Finance Data').document(u'sensex').update(data)
        print("Data added in Database", data)
    except Exception as e:
        print("Error while getting SENSEX Data::::", e)


def get_nifty():
    URL = "https://in.finance.yahoo.com/quote/%5ENSEI?p=%5ENSEI"
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        div = soup.find('div', attrs={'class': 'D(ib) Mend(20px)'})
        div = div.findAll('span')

        nifty_value = str(div[0].text)

        change = str(div[1].text).split(' ')
        nifty_change = change[0]
        nifty_pchange = change[1]

        nifty_timestamp = str(div[2].text)

        change_ispositive = None
        pchange_ispositive = None
        if(nifty_change[0] == '+'):
            change_ispositive = True
        else:
            change_ispositive = False

        if(nifty_pchange[1] == '+'):
            pchange_ispositive = True
        else:
            pchange_ispositive = False

        data = {
            "nifty_value": nifty_value,
            "change": nifty_change,
            "pchange": nifty_pchange,
            "nifty_ispositive": change_ispositive,
            "pchange_ispositive": pchange_ispositive,
            "lastUpdated": datetime.datetime.now(tz=tz)
        }

        db.collection(u'Finance Data').document(u'nifty').update(data)
        print("Data added in Database", data)
    except Exception as e:
        print("Error while getting NIFTY Data:::::", e)


def get_gold_rates():
    URL = "https://www.goodreturns.in/gold-rates/#Indian+Major+Cities+Gold+Rates+Today"

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        gold_table = soup.findAll('table')[1]
        tola_row = gold_table.findAll('tr')[3]

        change = tola_row.find('span').text.strip()

        row_data = tola_row.findAll('td')

        gold_rate = row_data[1].text
        gold_rate_yesterday = row_data[2].text

        data = {
            "rate_change": change,
            "gold_rate": gold_rate,
            "gold_rate_yesterday": gold_rate_yesterday,
            "lastUpdated": datetime.datetime.now(tz=tz)
        }

        db.collection(u'Finance Data').document(u'gold').update(data)
        print("Data added in Database", data)
    except Exception as e:
        print("Error while getting GOLD Rates::::", e)


def get_silver_rates():
    URL = "https://www.goodreturns.in/silver-rates/#Indian+Major+Cities+Silver+Rates+Today"

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        silver_table = soup.find('table')
        tola_row = silver_table.findAll('tr')[3]

        change = tola_row.find('span').text.strip()

        row_data = tola_row.findAll('td')

        silver_rate = row_data[1].text
        silver_rate_yesterday = row_data[2].text

        data = {
            "rate_change": change,
            "silver_rate": silver_rate,
            "silver_rate_yesterday": silver_rate_yesterday,
            "lastUpdated": datetime.datetime.now(tz=tz)
        }

        db.collection(u'Finance Data').document(u'silver').update(data)
        print("Data added in Database", data)
    except Exception as e:
        print("Error while getting SILVER Rates::::", e)


def get_news():
    url = "https://bing-news-search1.p.rapidapi.com/news/search"

    querystring = {"q": "finance", "count": "100",
                   "freshness": "Day", "textFormat": "Raw", "safeSearch": "Off"}

    headers = {
        'x-bingapis-sdk': "true",
        'x-rapidapi-key': "4dac98df60msh691f1232fed0d9ap170cabjsna864eb3f1b87",
        'x-rapidapi-host': "bing-news-search1.p.rapidapi.com"
    }

    try:
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        response = response.json()

        news_array = response["value"]
        push_news = []
        for news in news_array:
            try: 
                image_url = news["image"]["thumbnail"]["contentUrl"]
            except:
                image_url = None
            data = {
                "headline" : news["name"],
                "description" : news["description"],
                "image_url" : image_url
            }
            push_news.append(data)
        db.collection(u'Finance Data').document(u'news').update({
            "news": push_news
        })
        print("News Data added in Database")
    except Exception as e:
        print("Error while getting NEWS::::", e)



if __name__ == '__main__':
    get_news()
