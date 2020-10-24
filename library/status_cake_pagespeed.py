#!/usr/bin/python
import json

import requests
from ansible.module_utils.basic import AnsibleModule


class StatusCake:
    def __init__(self, module, username, api_key, name, url, state,
                 location, check_rate, contact,
                 alert_smaller, alert_bigger, alert_slower):
        self.headers = {"Username": username, "API": api_key}
        self.module = module
        self.name = name
        self.url = url
        self.state = state
        self.location = location
        self.check_rate = check_rate
        self.contact = contact
        self.alert_smaller = alert_smaller
        self.alert_bigger = alert_bigger
        self.alert_slower = alert_slower

    def check_response(self, resp):
        if resp['success'] is False or resp['message'] == 'No changes detected.':
            self.module.exit_json(changed=False, meta=resp['message'])
        else:
            self.module.exit_json(changed=True, meta=resp['message'])

    def check_test(self):
        API_URL = "https://app.statuscake.com/API/Pagespeed"
        response = requests.get(API_URL, headers=self.headers)
        json_object = response.json()

        for item in json_object['data']:
            if item['Title'] == self.name:
                return item['ID']

    def manage_test(self):
        data = {
            "name": self.name,
            "website_url": self.url,
            "location_iso": self.location,
            "checkrate": self.check_rate,
            "contact_groups": self.contact,
            "alert_smaller": self.alert_smaller,
            "alert_bigger": self.alert_bigger,
            "alert_slower": self.alert_slower
        }

        test_id = self.check_test()
        print(test_id)
        API_URL = "https://app.statuscake.com/API/Pagespeed/Update"
        if self.state == 'present':
            if test_id:
                data['id'] = test_id
            response = requests.post(API_URL, headers=self.headers, data=data)
        elif self.state == 'absent':
            if not test_id:
                self.module.exit_json(changed=False, meta='No test to delete with the specified name')
            data['id'] = int(test_id)
            API_URL = "https://app.statuscake.com/API/Pagespeed/Update?id=" + str(test_id)
            response = requests.delete(API_URL, headers=self.headers, data=data)
        self.check_response(response.json())


def main():
    fields = {
        "username": {"required": True, "type": "str"},
        "api_key": {"required": True, "type": "str", "no_log": True},
        "name": {"required": True, "type": "str"},
        "url": {"required": True, "type": "str"},
        "state": {"required": True, "choices": ['present', 'absent'], "type": "str"},
        "location": {"required": False, "type": "str"},
        "check_rate": {"required": False, "default": 300, "type": "int"},
        "contact": {"required": False, "type": "str"},
        "alert_smaller": {"required": False, "default": 0, "type": "int"},
        "alert_bigger": {"required": False, "default": 0, "type": "int"},
        "alert_slower": {"required": False, "default": 0, "type": "int"}
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

    username = module.params['username']
    api_key = module.params['api_key']
    name = module.params['name']
    url = module.params['url']
    state = module.params['state']
    location = module.params['location']
    check_rate = module.params['check_rate']
    contact = module.params['contact']
    alert_smaller = module.params['alert_smaller']
    alert_bigger = module.params['alert_bigger']
    alert_slower = module.params['alert_slower']


    test_object = StatusCake(module, username, api_key, name, url, state,
                             location, check_rate, contact,
                             alert_smaller, alert_bigger, alert_slower)
    test_object.manage_test()


if __name__ == '__main__':
    main()
