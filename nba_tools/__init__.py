import urllib.request
from pprint import pprint
from html_table_parser import HTMLTableParser
import pandas as pd
from datetime import datetime

# Opens a website and read its
# binary contents (HTTP Response Body)
def url_get_contents(url):

    # Opens a website and read its
    # binary contents (HTTP Response Body)

    #making request to the website
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)

    #reading contents of the website
    return f.read()


def get_bbref_results(year, month_list):
    urls = []
    return_df = pd.DataFrame()
    for month in month_list:
        new_url = f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html'
        urls.append(new_url)

    for url in urls:
        # defining the html contents of a URL.
        xhtml = url_get_contents(url).decode('utf-8')

        # Defining the HTMLTableParser object
        p = HTMLTableParser()

        # feeding the html contents in the
        # HTMLTableParser object
        p.feed(xhtml)

        df = pd.DataFrame(p.tables[0][1::], columns=p.tables[0][0])

        df['Date'] = pd.to_datetime(df['Date'])

        df.columns = ['date', 'start', 'away', 'away_pts', 'home', 'home_pts', 'box_score', 'ot', 'attend', 'notes']

        today = datetime.date(datetime.now()).strftime('%Y-%m-%d')

        df = df.loc[df['date'] < today]

        df.drop(['box_score', 'attend', 'notes'], axis=1, inplace=True)

        return_df = return_df.append(df)

    return return_df


def get_team_ratings(years):
    urls = []
    return_df = pd.DataFrame()
    for year in years:
        new_url = f'https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html'
        urls.append(new_url)

    for url in urls:
        # defining the html contents of a URL.
        xhtml = url_get_contents(url).decode('utf-8')

        # Defining the HTMLTableParser object
        p = HTMLTableParser()

        # feeding the html contents in the
        # HTMLTableParser object
        p.feed(xhtml)

        df = pd.DataFrame(p.tables[0][2::], columns=p.tables[0][1])

        return_df = return_df.append(df)

    return return_df


def daily_team_ratings(year):
    today = datetime.date(datetime.now()).strftime('%Y-%m-%d')

    today_df = get_team_ratings([year])

    today_df['date'] = today

    today_df.to_csv(f'./ratings/{year}/20-21.csv', mode='a', header=False, index=False)