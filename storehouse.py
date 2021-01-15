import re
import toml
import json
import logging
import requests_cache
import requests
from pymemcache.client.base import Client
from optparse import OptionParser as op
from netaddr import IPSet, IPNetwork, IPAddress

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class ThreatList(object):
    '''
    Creates a feed object that allows for easier interaction with each
    individual threat feed
    '''

    def __init__(self, data):
        '''
        Initializes the Feed object
        :param data: A dict that builds the object
        '''
        self.last_fetched = None
        self.__dict__.update(data)

    def fetch(self, config):
        '''
        Fetches a list from the destination URL and pushes the files
        to memcached
        '''

        logging.info('Fetching list information for "{}" from {}.'.format(self.name, self.url))

        session = requests.Session()

        if hasattr(self, 'disabled') and self.disabled:
            logging.info('Skipping list "{}" as it is disabled in the list config.'.format(self.name))
            return
        
        if config['proxy']['enabled']:
            session.proxies = {"http": config['proxy']['server'], "https": config['proxy']['server']}
            session.auth = requests.auth.HTTPProxyAuth(config['proxy']['proxy_user'], config['proxy']['proxy_password'])

        try:
            result = session.get(self.url)
            if result.status_code == 200:
                
                if self.format == "cidr":
                    for c in re.findall(r"((?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?))", result.text):
                        self.to_memcached(c, self.format, config)
                    
        except Exception as e:
            print(e)

    def to_memcached(self, value, format, config):
        '''
        Pushes a value to memcached using a namespace
        that matches the type of value
        '''

        if format == 'cidr':
            key = 'cidr_{}'.format(value)

        client = Client('127.0.0.1:11211')
        client.set(key, value)
        return


def load_config(path="config.toml"):
    '''
    Loads a config from a file on disk
    :param path: the file path to load from
    '''

    logging.info('Loading config from "{}".'.format(path))
    config = None
    try:
        with open(path) as f:
            config = f.read()
            config = toml.loads(config)
        return config
    except FileNotFoundError:
        logging.error('Configuration File "{}" not found.'.format(path))
        exit(1)    
    

def load_lists(path='lists.json'):
    '''
    Loads a config from a file on disk
    :param path: the file path to load from
    '''
    
    logging.info('Loading lists from "{}".'.format(path))
    lists = None
    try:
        with open(path) as f:
            lists = f.read()
            lists = json.loads(lists)
            lists = [ThreatList(l) for l in lists]
        return lists
    except FileNotFoundError:
        logging.error('Lists file "{}" not found.'.format(path))
        exit(1)

def process_list(url, format, type):
    raise NotImplementedError


if __name__ == "__main__":

    config =  load_config()

    lists = load_lists(path=config['main']['list_path'])

    for l in lists:
        l.fetch(config)
