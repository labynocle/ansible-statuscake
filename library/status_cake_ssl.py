#!/usr/bin/python
import json

import requests
from ansible.module_utils.basic import AnsibleModule


class StatusCakeSSL:
    def __init__(self, module, username, api_key, domain, state, check_rate, contact,
                 alert_at, alert_expiry, alert_reminder, alert_broken, alert_mixed):
        self.headers = {"Username": username, "API": api_key}
        self.module = module
        self.domain = domain
        self.state = state
        self.contact = contact
        self.check_rate = check_rate
        self.alert_at = alert_at
        self.alert_expiry = alert_expiry
        self.alert_reminder = alert_reminder
        self.alert_broken = alert_broken
        self.alert_mixed = alert_mixed

    def check_response(self, resp):
        if resp['Success'] is False:
            self.module.exit_json(changed=False, meta=resp['Message'])
        else:
            self.module.exit_json(changed=True, meta=resp['Message'])

    def check_test(self):
        API_URL = "https://app.statuscake.com/API/SSL"
        response = requests.put(API_URL, headers=self.headers)
        json_object = response.json()

        for item in json_object:
            if item['domain'] == self.domain:
                return item['id']

    def manage_test(self):
        data = {
            "domain": self.domain,
            "contact_groups": self.contact,
            "checkrate": self.check_rate,
            "alert_at": self.alert_at,
            "alert_expiry": self.alert_expiry,
            "alert_reminder": self.alert_reminder,
            "alert_broken": self.alert_broken,
            "alert_mixed": self.alert_mixed
        }

        test_id = self.check_test()

        if self.state == 'present':
            API_URL = "https://app.statuscake.com/API/SSL/Update"
            if test_id:
                data['id'] = test_id
            response = requests.put(API_URL, headers=self.headers, data=data)
        elif self.state == 'absent':
            if not test_id:
                self.module.exit_json(changed=False, meta='No test to delete with the specified domain')
            API_URL = "https://app.statuscake.com/API/SSL/Update?id=" + test_id
            response = requests.delete(API_URL, headers=self.headers)
        self.check_response(response.json())


def main():
    fields = {
        "username": {"required": True, "type": "str"},
        "api_key": {"required": True, "type": "str"},
        "domain": {"required": True, "type": "str"},
        "state": {"required": True, "choices": ['present', 'absent'], "type": "str"},
        "contact": {"required": True, "type": "int"},
        "check_rate": {"required": False, "default": 300, "choices": [300,600,3600,86400,2073600] ,"type": "int"},
        "alert_at": {"required": False, "default": "30,60,65", "type": "str"},
        "alert_expiry": {"required": False, "default": True, "type": "bool"},
        "alert_reminder": {"required": False, "default": True, "type": "bool"},
        "alert_broken": {"required": False, "default": True, "type": "bool"},
        "alert_mixed": {"required": False, "default": True, "type": "bool"},
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

    username = module.params['username']
    api_key = module.params['api_key']
    domain= module.params['domain']
    state = module.params['state']
    check_rate = module.params['check_rate']
    contact = module.params['contact']
    alert_at = module.params['alert_at']
    alert_expiry = module.params['alert_expiry']
    alert_reminder = module.params['alert_reminder']
    alert_broken = module.params['alert_broken']
    alert_mixed = module.params['alert_mixed']

    test_object = StatusCakeSSL(module, username, api_key, domain, state, check_rate, contact,
                             alert_at, alert_expiry, alert_reminder, alert_broken, alert_mixed)

    test_object.manage_test()


if __name__ == '__main__':
    main()
