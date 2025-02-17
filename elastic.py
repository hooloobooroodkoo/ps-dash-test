from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import utils.helpers as hp
import pandas as pd
import getpass

user, passwd, mapboxtoken = None, None, None
with open("creds.key") as f:
    user = f.readline().strip()
    passwd = f.readline().strip()

def ConnectES():
    global user, passwd
    credentials = (user, passwd)
    try:
        if getpass.getuser() == 'petya':
            es = Elasticsearch('http://localhost:9200', timeout=200, http_auth=credentials, max_retries=20)
        else:
            es = Elasticsearch([{'host': 'atlas-kibana.mwt2.org', 'port': 9200, 'scheme': 'https'}],
                                    timeout=240, verify_certs=False, http_auth=credentials, max_retries=10)
        print('Success' if es.ping()==True else 'Fail')
        return es
    except Exception as error:
        print (">>>>>> Elasticsearch Client Error:", error)
        