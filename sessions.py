from urllib import response
import requests
import time
import sys

for i in range(21):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)

class Session:

    def __init__(self,token):
        self.config()
        self.token=token
        self.results=[]
        self.row_count=None
        self.last_response=None
        self.error_iterator=0


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

    def goodRequest(self,resposne):
        sc=response.status_code
        fail_string=f'Failed request with status {sc}: '
        if sc==200:
            return True
        elif sc==401:
            print(fail_string+'Error with authentication')
            return False
        elif sc==403:
            print(fail_string+'Token not included or invalid')
            return False
        elif sc==404:
            print(fail_string+'URL Not Found')
            return False
        elif sc==429:
            print(fail_string+'Token exceeded allowed requests')
            return False
        elif sc==502:
            print(fail_string+'Server not responding')
            return False
        elif sc==504:
            print(fail_string+'Request is taking too long')
            return False
        else:
            pass

    def basic_request(self,params,additional_url=''):
        response=self.get_response(params,additional_url)
        if self.goodRequest(response):
            results=self.get_results(response)
            self.error_iterator=0
            return results
        else:
            self.error_iterator+=1
            if self.error_iterator==5:
                print('Couldn\'t solve error')
                return []
            print(f'Retrying in {self.error_iterator*10} seconds')
            time.sleep(self.error_iterator)
            self.basic_request(self,params,additional_url)

    

    def full_request(self,params,additional_url=''):
        initial_offset=self.offset
        initial_response=self.get_response(params,additional_url)
        self.row_count=initial_response.json().get('count')
        for offset in range(initial_offset+self.limit,self.row_count,self.limit):
            self.offset=offset
            results=self.basic_request(params,additional_url)
            if self.error_iterator==5: break
            self.show_process_status(offset,self.row_count)
            self.results+=results
            time.sleep(self.sleep_time)
        self.show_process_status(self.row_count,self.row_count)

    @staticmethod
    def show_process_status(i,max_num):
        p=int(i*100/max_num)
        sys.stdout.write('\r')
        sys.stdout.write(f"Processing: {p}%")
        sys.stdout.flush()