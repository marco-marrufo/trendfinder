from pytrends.request import TrendReq

def get_trends(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    #pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1)
    pytrends.build_payload([keyword], timeframe='today 3-m', geo='US', gprop='')
    return pytrends.interest_over_time()
