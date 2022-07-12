import requests
import time
import sys

class Session:

    def __init__(self,token):
        self.config()
        self.token=token
        self.results=[]
        self.row_count=None
        self.last_response=None
        self.error_iterator=0


    def config(self,limit=100,offset=0,basic_url="https://sipub.api.coordinador.cl/sipub/api/v2/recursos/",sleep_time=0.1):
        self.limit=limit
        self.offset=offset
        self.basic_url=basic_url
        self.sleep_time=sleep_time

    def get_response(self,params,additional_url=''):
        params.update({"limit":self.limit,"offset":self.offset, "user_key":self.token})
        url=self.basic_url + additional_url
        response = requests.get(url, params=params)
        self.last_response=response
        return response

    def get_results(self,response):
        results=response.json().get('results')
        return results

    def goodRequest(self,response):
        sc=response.status_code
        fail_string=f'Failed request with status {sc}: '
        if sc==200:
            return True
        elif sc==401:
            raise(fail_string+'Error with authentication')
           
        elif sc==403:
            raise(fail_string+'Token not included or invalid')
            
        elif sc==404:
            raise(fail_string+'URL Not Found')
            
        elif sc==429:
            raise (fail_string+'Token exceeded allowed requests')
            
        elif sc==502:
            print(fail_string+'Server not responding')
            return False
        elif sc==504:
            print(fail_string+'Request is taking too long')
            return False
        else:
            print(fail_string+'Unknown error')
            return False

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
        if not self.goodRequest(initial_response): 
            print('First response with error, returning None')
            return
        self.row_count=initial_response.json().get('count')
        
        if self.row_count==0:
            raise Exception('No results found')

        print(f'Request contains {self.row_count} rows \n')
        initial_results=self.get_results(initial_response)
        self.results+=initial_results
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
        p=int(i*100/max_num) if max_num>0 else 100
        sys.stdout.write('\r')
        sys.stdout.write(f"Processing: {p}%")
        sys.stdout.flush()