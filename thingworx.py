import requests
import json


class Thing:
    def __init__(self, server, app_key, unique_id):
        self.server = server
        self.app_key = app_key
        self.unique_id = unique_id

    def register_thing(self):
        try:
            self.create_thing()
            # the newly created Thing has to be enabled
            self.post_to_service('EnableThing')
            # after the new Thing is enabled it must be restarted
            self.post_to_service('RestartThing')
            # add properties
            self.post_to_service('AddPropertyDefinition', {'name': 'temperature', 'type': 'NUMBER'})
            self.post_to_service('AddPropertyDefinition', {'name': 'pressure', 'type': 'NUMBER'})
            self.post_to_service('AddPropertyDefinition', {'name': 'humidity', 'type': 'NUMBER'})
            self.post_to_service('AddPropertyDefinition', {'name': 'sw_yellow', 'type': 'BOOLEAN'})
            self.post_to_service('AddPropertyDefinition', {'name': 'sw_green', 'type': 'BOOLEAN'})
            self.post_to_service('AddPropertyDefinition', {'name': 'sw_blue', 'type': 'BOOLEAN'})
            # after changes to a Thing's structure it must be restarted
            self.post_to_service('RestartThing')
        except Exception, e:
            self.delete_thing()
            raise e

    def create_thing(self):
        url = 'http://' + self.server + '/Thingworx/Resources/EntityServices/Services/CreateThing'
        prms = {'appKey': self.app_key}
        hdrs = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            'name': self.unique_id,
            'thingTemplateName': 'GenericThing'
        }

        print 'POST ' + url
        r = requests.post(url, params=prms, headers=hdrs, data=json.dumps(data))
        print r.status_code

        return r.ok

    def post_to_service(self, service, data=None):
        url = 'http://' + self.server + '/Thingworx/Things/' + self.unique_id + '/Services/' + service
        prms = {'appKey': self.app_key}
        hdrs = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        text = json.dumps(data) if data else None

        print 'POST ' + url
        print 'data: ' + (text if text else 'None')
        r = requests.post(url, params=prms, headers=hdrs, data=text)
        print r.status_code
        if not r.ok:
            raise Exception('Failed to post to %s (status=%d)' % (service, r.status_code))

        return r.ok

    def add_property_value(self, name, value):
        url = 'http://' + self.server + '/Thingworx/Things/' + self.unique_id + '/Properties/' + name
        prms = {'appKey': self.app_key}
        hdrs = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {name: str(value)}
        text = json.dumps(data)
        print 'PUT ' + url
        print 'data: ' + text
        r = requests.put(url, params=prms, headers=hdrs, data=text)
        print r.status_code
        if not r.ok:
            raise Exception('Failed to put to %s (status=%d)' % (name, r.status_code))

        return r.status_code

    def get_thing(self):
        url = 'http://' + self.server + '/Thingworx/Things/' + self.unique_id
        prms = {'appKey': self.app_key}
        hdrs = {
            'Accept': 'application/json'
        }

        print 'GET ' + url
        r = requests.get(url, params=prms, headers=hdrs)
        print r.status_code

        return r.ok

    def delete_thing(self):
        url = 'http://' + self.server + '/Thingworx/Things/' + self.unique_id
        prms = {'appKey': self.app_key}
        hdrs = {
            'Content-Type': 'application/json'
        }

        print 'DELETE ' + url
        r = requests.delete(url, params=prms, headers=hdrs)
        print r.status_code

        return r.ok
