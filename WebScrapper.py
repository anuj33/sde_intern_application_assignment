import urllib2
from bs4 import BeautifulSoup
import requests
import hmac, hashlib
import base64
import json


class WebScrapper:
    def __init__(self):
        pass
    #using wikipedia to scrape the information as it is most versatile resource available on net
    #can't figure out a definitive algo to extract required info
    def find_treatment_options_for_medical_condition(self, medical_condition):
        try:
            uri = "https://en.wikipedia.org/wiki/{}".format(medical_condition)
            resp = urllib2.urlopen(uri)
            soup = BeautifulSoup(resp, 'html.parser')
            headers = [a['href'].replace("#", "") for a in soup.find_all('a', href=True) if a.text]
            idx = headers.index("Management") #management contains list of treatments available
            treatment = headers[idx+1:idx+3] #taking best ways to diagnose the disease
            return {"treatment_options" : treatment}
        except:
            raise ValueError({"error" :"unable to scrape data for the give medical condition = {} from wikipedia".format(medical_condition)})


