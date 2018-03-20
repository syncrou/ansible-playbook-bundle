import os
import json
import re
import pdb
import requests

class MiqConnect(object):
    """
        MIQ REST API operations
    """

    def __init__(self, opts):
        self._server = opts['server']
        self._service = opts['service']
        self._username = opts['username']
        self._password = opts['password']
        self._validate_certs = opts['validate-certs']
        self._debug = opts['debug'] or None
        self._params = dict()
        self._credentials = (self._username, self._password)
        self._auth = self._build_auth()

    @property
    def url(self):
        """ The URL used to access the REST API """
        return self._build_url()


    def _build_url(self):
        """
            Using any type of href input, build out the correct url
        """

        return "http://" + self._server + '/api/' + self._parse_slug()


    def _parse_slug(self):
        """
            Decode the href_slug
        """
        item = self._service
        if isinstance(item, str):
            slug = item.split("::")
            if len(slug) == 2:
                return slug[1]
            return item


    def _build_auth(self):
        self._headers = {'Content-Type': 'application/json; charset=utf-8'}
        self._params['validate_certs'] = self._validate_certs
        self._params['force_basic_auth'] = True


    def get(self):
        """
            Get any attribute, object from the REST API
        """
        result = requests.get(self.url, auth=self._credentials)
        if result.status_code == 200:
            return result.json()
        else:
            return result.status_code


    def set(self, post_dict):
        """
            Set any attribute, object from the REST API (POST)
        """
        #post_data = json.dumps(dict(action=post_dict['action'], resource=post_dict['resource']))
        #return self._build_result('post', post_data)

class ServiceTemplate(MiqConnect):
    """
        Grab a service template from miq, and parse it
    """

    def convert(self):
        """
            Convert a ServiceTemplate into an apb.yaml file
        """
        resp = self.get()
        print resp

def check_for_inited_apb():
    """
        Make sure we're in an existing APB directory
    """
    # check for Dockerfile, apb.yml, Makefile
    for fname in ('Dockerfile', 'apb.yml', 'Makefile'):
        if os.path.isfile(fname):
            pass
        else:
            raise Exception("Missing filename: {fname}, Are you running inside an apb directory?".format(fname=fname))



def cmdrun_add(**kwargs):
    """ Run MIQ apb operations """
    check_for_inited_apb()
    temp = ServiceTemplate(kwargs)
    return temp.convert()
