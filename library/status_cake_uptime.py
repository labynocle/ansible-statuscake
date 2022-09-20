#!/usr/bin/python
import json

import requests
from ansible.module_utils.basic import AnsibleModule

class StatusCake:
    def __init__(self, module, api_key, name, website_url, state, tags, status_codes_csv,
                            regions, check_rate, test_type, basic_username, basic_password, contact_groups,
                            tcp_port, user_agent, follow_redirects, enable_ssl_alert, paused,
                            trigger_rate, confirmation, do_not_find, find_string, custom_header,
                            post_body, post_raw):
        self.headers = {
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.module = module
        self.name = name
        self.website_url = website_url
        self.state = state
        self.tags = tags
        self.status_codes_csv = status_codes_csv
        self.regions = regions
        self.check_rate = check_rate
        self.test_type = test_type
        self.basic_username = basic_username
        self.basic_password = basic_password
        self.contact_groups = contact_groups
        self.tcp_port = tcp_port
        self.user_agent = user_agent
        self.follow_redirects = follow_redirects
        self.enable_ssl_alert = enable_ssl_alert
        self.paused = paused
        self.trigger_rate = trigger_rate
        self.confirmation = confirmation
        self.do_not_find = do_not_find
        self.find_string = find_string
        self.custom_header = custom_header
        self.post_body = post_body
        self.post_raw = post_raw


    def check_if_exist(self, page_index=1):
        params = {
            "limit": 100,
            "page": page_index
        }
        API_URL = "https://api.statuscake.com/v1/uptime"
        response = requests.get(API_URL, headers=self.headers, params=params)
        json_object = response.json()

        for item in json_object['data']:
            if item['name'] == self.name:
                return item['id']

        if page_index != json_object['metadata']['page_count'] and page_index < json_object['metadata']['page_count']:
            page_index += 1
            return self.check_if_exist(page_index)


    def manage_test(self):
        data = {
            "name": self.name,
            "website_url": self.website_url,
            "state": self.state,
            "tags[]": self.tags,
            "status_codes_csv": self.status_codes_csv,
            "regions[]": self.regions,
            "check_rate": self.check_rate,
            "test_type": self.test_type,
            "basic_username": self.basic_username,
            "basic_password": self.basic_password,
            "contact_groups[]": self.contact_groups,
            "tcp_port": self.tcp_port,
            "user_agent": self.user_agent,
            "follow_redirects": self.follow_redirects,
            "enable_ssl_alert": self.enable_ssl_alert,
            "paused": self.paused,
            "trigger_rate": self.trigger_rate,
            "confirmation": self.confirmation,
            "do_not_find": self.do_not_find,
            "find_string": self.find_string,
            "post_raw": self.post_raw
        }

        if self.custom_header:
            data['custom_header'] = self.custom_header
        if self.post_body:
            data['post_body'] = self.post_body

        test_id = self.check_if_exist()

        API_URL = "https://api.statuscake.com/v1/uptime"

        if self.state == 'present':

            if test_id:
                API_URL += "/" + str(test_id)
                response = requests.put(API_URL, headers=self.headers, data=data)
                if response.status_code == 204: self.module.exit_json(changed=True, meta='Test updated with success')
            else:
                response = requests.post(API_URL, headers=self.headers, data=data)  # must return 201 et y a
                if response.status_code == 201: self.module.exit_json(changed=True, meta='Test created with success')

        elif self.state == 'absent':
            if not test_id:
                self.module.exit_json(changed=False, meta='No test to delete with the specified name: ' + self.name)
            API_URL += "/" + str(test_id)
            response = requests.delete(API_URL, headers=self.headers, data=data)
            if response.status_code == 204: self.module.exit_json(changed=True, meta='Test deleted with success')

        self.module.fail_json(msg="Problem when trying to update/delete the test with the specified name: " + self.name)

def main():
    fields = {
        "api_key": {"required": True, "type": "str", "no_log": True},
        "name": {"required": True, "type": "str"},
        "website_url": {"required": True, "type": "str"},
        "state": {"required": True, "choices": ['present', 'absent'], "type": "str"},
        "tags": {"required": False, "type": "list"},
        "status_codes_csv": {"required": False, "type": "str"},
        "regions": {"required": False, "type": "list"},
        "check_rate": {"required": False, "choices": [30, 60, 300, 900, 1800, 3600, 86400], "default": 300, "type": "int"},
        "test_type": {"required": False, "choices": ['HTTP', 'TCP', 'PING'], "type": "str"},
        "basic_username": {"required": False, "default": "", "type": "str"},
        "basic_password": {"required": False, "default": "", "type": "str", "no_log": True},
        "contact_groups": {"required": False, "type": "list"},
        "port": {"required": False, "type": "int"},
        "user_agent": {"required": False, "default": "StatusCake Agent", "type": "str"},
        "follow_redirects": {"required": False, "default": False, "type": "bool"},
        "enable_ssl_alert": {"required": False, "default": False, "type": "bool"},
        "paused": {"required": False, "default": False, "type": "bool"},
        "trigger_rate": {"required": False, "default": 0, "type": "int"},
        "confirmation": {"required": False, "default": 3, "type": "int"},
        "do_not_find": {"required": False, "default": False, "type": "bool"},
        "find_string": {"required": False, "type": "str"},
        "custom_header": {"required": False, "type": "dict"},
        "post_raw": {"required": False, "type": "str"},
        "post_body": {"required": False, "type": "dict"}
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

    api_key = module.params['api_key']
    name = module.params['name']
    website_url = module.params['website_url']
    state = module.params['state']
    tags = module.params['tags']
    status_codes_csv = module.params['status_codes_csv']
    regions = module.params['regions']
    check_rate = module.params['check_rate']
    test_type = module.params['test_type']
    basic_username = module.params['basic_username']
    basic_password = module.params['basic_password']
    contact_groups = module.params['contact_groups']
    tcp_port = module.params['port']
    user_agent = module.params['user_agent']
    follow_redirects = module.params['follow_redirects']
    enable_ssl_alert = module.params['enable_ssl_alert']
    paused = module.params['paused']
    trigger_rate = module.params['trigger_rate']
    confirmation = module.params['confirmation']
    do_not_find = module.params['do_not_find']
    find_string = module.params['find_string']
    custom_header = module.params['custom_header']
    post_body = module.params['post_body']
    post_raw = module.params['post_raw']

    if custom_header:
        custom_header = json.dumps(custom_header)
    if post_body:
        post_body = json.dumps(post_body)

    test_object = StatusCake(module, api_key, name, website_url, state, tags, status_codes_csv,
                            regions, check_rate, test_type, basic_username, basic_password, contact_groups,
                            tcp_port, user_agent, follow_redirects, enable_ssl_alert, paused,
                            trigger_rate, confirmation, do_not_find, find_string, custom_header,
                            post_body, post_raw)

    test_object.manage_test()


if __name__ == '__main__':
    main()
