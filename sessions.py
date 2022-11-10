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
        self.token_list  = ["fd8a8857a0da5f8a208316428ad9790a",
                            "905df7a50919527cdb5075fb356be81c",
                            "850da6e5730480c91b85c93f62c60f8c",
                            "aad372f1da033807985c3c6b0ac0073b"
                            "3b10b96b9299bd66e8686dc0a749f0ab"]

        self.headers = headers = {
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                        'Connection': 'keep-alive',
                        'Origin': 'https://www.coordinador.cl',
                        'Referer': 'https://www.coordinador.cl/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70',
                        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

    def config(self,limit=100,offset=0,basic_url="https://sipub.api.coordinador.cl/api/v2/recursos/",sleep_time=0.1):
        self.limit=limit
        self.offset=offset
        self.basic_url=basic_url
        self.sleep_time=sleep_time

    def get_response(self,params,additional_url=''):
        params.update({"limit":self.limit,"offset":self.offset, "user_key":self.token})
        url=self.basic_url + additional_url
        if additional_url=="demanda_sistema_real":
            try:
                response = requests.get(url, params=params, verify=True)
            except:  
                response = requests.get(url, params=params, headers = self.headers, verify=True)
        else:
            response = requests.get(url, params=params, verify=True)
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