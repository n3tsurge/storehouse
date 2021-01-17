# storehouse.py

import re
import toml
import json
import logging
import requests_cache
import requests
import ipaddress
from pymemcache.client.base import Client
from optparse import OptionParser as op
from netaddr import IPSet, IPNetwork, IPAddress
from flask import Flask

# Configure a logging format for the feeds that matches the Flask logging format
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

        session = requests.Session()

        if hasattr(self, 'disabled') and self.disabled:
            logging.info('Skipping list "{}" as it is disabled in the list config.'.format(self.name))
            return
        else:
            logging.info('Fetching list information for "{}" from {}.'.format(self.name, self.url))
        
        if config['proxy']['enabled']:
            session.proxies = {"http": config['proxy']['server'], "https": config['proxy']['server']}
            session.auth = requests.auth.HTTPProxyAuth(config['proxy']['proxy_user'], config['proxy']['proxy_password'])

        try:
            result = session.get(self.url)
            if result.status_code == 200:
                
                if self.format == "cidr":
                    for c in re.findall(r"((?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?))", result.text):
                        self.to_memcached(c, self.format, config)
                else:
                    for c in result.text.split('\n'):
                        self.to_memcached(c, self.format, config)
                    
        except Exception as e:
            print(e)

    def to_memcached(self, value, format, config):
        '''
        Pushes a value to memcached using a namespace
        that matches the type of value
        '''

        if format == 'cidr':
            key = 'cidr_{}'
        if format == 'ip':
            key = 'ip_{}'

        key = key.format(value)

        client = Client('127.0.0.1:11211')
        client.set(key, json.dumps({"value": value, "list_name": self.name, "list_url": self.url}))
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

    # Create the memcached client
    client = Client('{}:{}'.format(config['memcached']['hostname'], str(config['memcached']['port'])))

    # Load all the list data
    lists = load_lists(path=config['main']['list_path'])
    for l in lists:
        l.fetch(config)
    logging.info('Finished loading threat feeds')

    # TODO: Spawn a feeder as a sub process that constantly refreshes the lists at a set interval

    # TODO: Launch flask for querying memcached

    logging.info('Launching web server')

    app = Flask(__name__)   

    @app.route('/')
    def index():
        return 'Hello'

    @app.route('/ip/<ip>')
    def ip_check(ip):
        '''
        Checks if an IP address is in any of the IP indicators
        '''
        if ipaddress.ip_address(ip):
            key = "ip_{}".format(ip)
            value = client.get(key)
            if value:
                return value.decode()
            else:
                return json.dumps({"value":"Not found"})
        else:
            return json.dumps({"value":"Invalid IP Address"})
        return json.dumps({"value":"Not found"})

    app.run()

    

