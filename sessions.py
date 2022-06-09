import requests
import time
import pandas as pd

class Session:

    def __init__(self,token):
        self.config()
        self.token=token
        self.results=[]
        self.row_count=None
        self.last_response=None


    def config(self,limit=100,offset=0,basic_url="https://sipub.coordinador.cl/api/v2/recursos/",sleep_time=0.1):
        self.limit=limit
        self.offset=offset
        self.basic_url=basic_url
        self.sleep_time=sleep_time

    def get_response(self,params,additional_url=''):
        params.update({"limit":self.limit,"offset":self.offset})
        headers={'authorization': f"Token {self.token}"}
        url=self.basic_url + additional_url
        response = requests.get(url, headers=headers, params=params)
        self.last_response=response
        return response

    def get_results(self,response):
        results=response.json().get('results')
        return results

    def basic_request(self,params,additional_url=''):
        response=self.get_response(params,additional_url)
        """
        Aqui debiese haber un response handler
        """
        results=self.get_results(response)
        return results

    def full_request(self,params,additional_url=''):
        initial_offset=self.offset
        initial_response=self.get_response(params,additional_url)
        self.row_count=initial_response.json().get('count')
        for offset in range(initial_offset+self.limit,self.row_count,self.limit):
            self.offset=offset
            results=self.basic_request(params,additional_url)
            self.results+=results
            time.sleep(self.sleep_time)

    def to_df(self):
        return pd.json_normalize(self.results)