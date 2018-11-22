#!/usr/bin/python
import json

import requests
from ansible.module_utils.basic import *  # noqa: F403


class StatusCake:

    def __init__(self, module, username, api_key, name, url, state, test_tags, check_rate, test_type, contact, tcp_port, user_agent,
                 status_codes, node_locations, follow_redirect, trigger_rate, final_location, find_string, custom_header):
        self.headers = {"Username": username, "API": api_key}
        self.module = module
        self.name = name
        self.url = url
        self.state = state
        self.test_tags = test_tags
        self.status_codes = status_codes
        self.node_locations = node_locations
        self.test_type = test_type
        self.contact = contact
        self.tcp_port = tcp_port
        self.user_agent = user_agent
        self.check_rate = check_rate
        self.follow_redirect = follow_redirect
        self.trigger_rate = trigger_rate
        self.final_location = final_location
        self.find_string = find_string
        self.custom_header = custom_header

    def check_response(self, resp):
        if resp['Success'] is False:
            self.module.exit_json(changed=False, meta=resp['Message'])
        else:
            self.module.exit_json(changed=True, meta=resp['Message'])

    def check_test(self):
        API_URL = "https://app.statuscake.com/API/Tests"
        response = requests.put(API_URL, headers=self.headers)
        json_object = response.json()

        for item in json_object:
            if item['WebsiteName'] == self.name:
                return item['TestID']

    def manage_test(self):
        data = {
            "WebsiteName": self.name, "WebsiteURL": self.url, "CheckRate": self.check_rate, "TestType": self.test_type,
            "TestTags": self.test_tags, "StatusCodes": self.status_codes, "NodeLocations": self.node_locations, "ContactGroup": self.contact,
            "Port": self.tcp_port, "UserAgent": self.user_agent, "FollowRedirect": self.follow_redirect, "TriggerRate": self.trigger_rate,
            "FinalEndpoint": self.final_location, "FindString": self.find_string, "CustomHeader": self.custom_header
        }

        test_id = self.check_test()

        if self.state == 'present':
            if test_id:
                data['TestID'] = test_id
            API_URL = "https://app.statuscake.com/API/Tests/Update"
            response = requests.put(API_URL, headers=self.headers, data=data)
        elif self.state == 'absent':
            if not test_id:
                self.module.exit_json(changed=False, meta='No test to delete with the specified name')
            data['TestID'] = test_id
            API_URL = "https://app.statuscake.com/API/Tests/Details"
            response = requests.delete(API_URL, headers=self.headers, data=data)
        self.check_response(response.json())


def main():
    fields = {
        "username": {"required": True, "type": "str"},
        "api_key": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "url": {"required": True, "type": "str"},
        "state": {"required": True, "choices": ['present', 'absent'], "type": "str"},
        "test_tags": {"required": False, "type": "str"},
        "status_codes": {"required": False, "type": "str"},
        "node_locations": {"required": False, "type": "str"},
        "follow_redirect": {"required": False, "type": "str"},
        "trigger_rate": {"required": False, "type": "str"},
        "check_rate": {"required": False, "default": 300, "type": "int"},
        "test_type": {"required": False, "choices": ['HTTP', 'TCP', 'PING'], "type": "str"},
        "contact": {"required": False, "type": "int"},
        "port": {"required": False, "type": "int"},
        "user_agent": {"required": False, "default": "StatusCake Agent", "type": "str"},
        "final_location": {"required": False, "type": "str"},
        "find_string": {"required": False, "type": "str"},
        "custom_header": {"required": False, "type": "dict"}
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)  # noqa: F405

    username = module.params['username']
    api_key = module.params['api_key']
    name = module.params['name']
    url = module.params['url']
    state = module.params['state']
    test_tags = module.params['test_tags']
    status_codes = module.params['status_codes']
    node_locations = module.params['node_locations']
    check_rate = module.params['check_rate']
    test_type = module.params['test_type']
    contact = module.params['contact']
    tcp_port = module.params['port']
    user_agent = module.params['user_agent']
    follow_redirect = module.params['follow_redirect']
    trigger_rate = module.params['trigger_rate']
    final_location = module.params['final_location']
    find_string = module.params['find_string']
    custom_header = module.params['custom_header']

    custom_header = json.dumps(custom_header)

    test_object = StatusCake(module, username, api_key, name, url, state, test_tags, check_rate, test_type, contact, tcp_port, user_agent,
                             status_codes, node_locations, follow_redirect, trigger_rate, final_location, find_string, custom_header)
    test_object.manage_test()


if __name__ == '__main__':
    main()
