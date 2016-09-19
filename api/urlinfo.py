import falcon
import binascii
from pymongo import MongoClient
from middleware import JSONTranslator
from middleware import RequireJSON


class URLInfo(object):
    bad_urls = {}

    def __init__(self):

        self.bad_urls = {
            '76233f96':
            {
                '76233f96': True,
                'b9bfeca4': ['3fae0229', 'b9bfeca4']
            }
        }

    def _compress_url(self,
                      hostname_port,
                      query_name=None,
                      query_string=None):

        crc32_hostname_port = "{:x}".format(
            binascii.crc32(bytearray(hostname_port, 'utf-8')))

        crc32_query_name = None
        if query_name:
            crc32_query_name = "{:x}".format(
                binascii.crc32(bytearray(query_name, 'utf-8')))

        crc32_query_string = None
        if query_string:
            crc32_query_string = "{:x}".format(
                binascii.crc32(bytearray(query_string, 'utf-8')))

        return crc32_hostname_port, crc32_query_name, crc32_query_string

    def _match(self, hostname_port, query_name=None, query_string=None):
        is_match = False
        paths = self.bad_urls.get(hostname_port, False)
        if paths:
            if self.bad_urls[hostname_port].get(hostname_port, False):
                is_match = True
            else:
                querys = self.bad_urls[hostname_port].get(query_name, False)
                if querys:
                    if query_name in self.bad_urls[hostname_port][query_name]:
                        is_match = True
                    else:
                        qs_list = self.bad_urls[hostname_port][query_name]
                        if query_string in qs_list:
                            is_match = True

        return is_match

    def on_get(self,
               req,
               resp,
               hostname_port,
               query_name=None):

        c_hp, c_qn, c_qs = self._compress_url(hostname_port,
                                              query_name,
                                              req.query_string)
        resp.status = falcon.HTTP_200
        req.context['result'] = str(self._match(c_hp, c_qn, c_qs))

    def on_post(self, req, resp, hostname_port, query_name=None):
        client = MongoClient('mongodb://mongodb:27017/')
        db = client.blurl_database
        c_hp, c_qn, c_qs = self._compress_url(hostname_port,
                                              query_name,
                                              req.query_string)
        uri = hostname_port
        if query_name:
            uri += "/" + query_name

            if req.query_string:
                uri += "?" + req.query_string,

        new_url = {
            'uri': uri,
            'hostname_port': c_hp,
            'query_name': c_qn,
            'query_string': c_qs,
        }
        query = {"uri": new_url['uri']}

        urls = db.urls
        result = urls.update(query, new_url, upsert=True)

        resp.status = falcon.HTTP_200
        req.context['result'] = str(result)


app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])
urlinfo = URLInfo()
template = '/urlinfo/1/{hostname_port}/{query_name}'
app.add_route(template, urlinfo)
template = '/urlinfo/1/{hostname_port}'
app.add_route(template, urlinfo)
