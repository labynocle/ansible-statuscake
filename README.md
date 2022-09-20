# Ansible-statuscake

This Ansible module setups/deletes a HTTP/TCP/PING test via the [StatusCake](https://www.statuscake.com) API.

:warning: the 30/09/2022th, the API used by this module will be deprecated.
I already start a MR to migrate to the new one, you can follow the work on
this MR: [feat: use APIv1](https://github.com/labynocle/ansible-statuscake/pull/13).
I try my best to be on time :pray:

## Requirements

* Ansible >=2.1
* Python >=3.4

## Installation

Just copy the **library/status_cake_*.py** in your playbook folder

## status_cake_uptime :: Example usage:

```
- hosts:      localhost

  tasks:
    - name: Create StatusCake tests
      status_cake_test:
        api_key: "som3thing1se3cret"               # Mandatory - StatusCake API key (cf: Manage API Keys - https://app.statuscake.com/User.php)
        state: "present"                           # Mandatory - If present the task will try to create/update the test, if absent the task will delete the test
        name: "Test for my website"                # Mandatory - Name of the check
        website_url: "https://mywebsite.com"       # Mandatory - URL or IP address of the server under test
        status_codes_csv: "404,500"                # Comma separated list of status codes that trigger an alert
        tags:                                      # List of tags
          - "something"
          - "somethingelse"
          - "anotherone"
        check_rate: 300                            # Number of seconds between checks
        test_type: "HTTP"                          # Uptime check type (HTTP/TCP/PING)
        # basic_username: "myUser"                 # Basic authentication username
        # basic_password: "myPassw0rd"             # Basic authentication password
        contact_groups:                            # List of contact group IDs
          - 1234
          - 42
        # port: 8080                               # Destination port for TCP checks
        user_agent: "Status Cake Monitoring"       # Custom user agent string set when testing
        follow_redirect: true                      # Whether to follow redirects when testing. Disabled by default
        enable_ssl_alert: true                     # Whether to send an alert if the SSL certificate is soon to expire - Disabled by default
        paused: true                               # Whether the check should be run - Disabled by default
        trigger_rate: 5                            # The number of minutes to wait before sending an alert - Default is 0
        confirmation: 5                            # Number of confirmation servers to confirm downtime before an alert is triggered - Default is 2
        regions:                                   # List of regions on which to run checks (retrieved from the GET /v1/uptime-locations endpoint)
          - "sao-polo"
          - "singapore"
        # find_string: "plop"                      # String to look for within the response. Considered down if not found
        # do_not_find: false                       # Whether to consider the check as down if the content is present within the response - Disabled by default
        # custom_header:                           # JSON object. Represents headers to be sent when making requests
        #  Header01: Plop
        #  Header02: Plip
```

:information_source: if `state` is `present`, the task will be always seen as
`changed`.

## Tips / Dirty quick win

### status_cake_test :: How to use `post_raw` with a JSON

Your `post_raw` ansible variable should be declared with a leading space:

```
my_post_raw: ' {"field1":"result1"}'
my_custom_headers:
  Content-Type: "application/json"
```

The leading space causes Ansible to not treat your string as JSON

Then you can use `my_post_raw` in your `status_cake_test` task without problem as following:

```
status_cake_test:
  ...
  custom_header: "{{ my_custom_headers }}"
  post_raw:      "{{ my_post_raw }}"
```

### how to automatically retrieve contact groups ID

Just launch the following commands:

```
$ export STATUSCAKE_API_KEY=XXXX

$ curl -s https://api.statuscake.com/v1/contact-groups \
  -H "Authorization: Bearer ${STATUSCAKE_API_KEY}" \
  | jq -r '.data[] | {name, id} | join(",")'
```

Then use these IDs to set the `contact_groups` parameter.

## Contributing

* Generate an API key on [StatusCake](https://app.statuscake.com/User.php) and export
it as `STATUSCAKE_API_KEY`
* Then just launch a test which will create a basic HTTP test:

```
$ export STATUSCAKE_API_KEY=XXXX

$ make test

{"changed": true, "meta": "Test updated with success", "invocation": {"module_args": {"api_key": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER", "name": "My first uptime :: google.com", "state": "present", "test_type": "HTTP", "website_url": "https://www.google.com", "check_rate": 3600, "status_codes_csv": "200,204,205", "user_agent": "Test ansible", "tags": "toto,titi", "follow_redirects": true, "trigger_rate": 10, "confirmation": 2, "basic_username": "", "basic_password": "", "enable_ssl_alert": false, "paused": false, "do_not_find": false, "regions": null, "contact_groups": null, "port": null, "find_string": null, "custom_header": null, "post_raw": null, "post_body": null}}}
```

## Links

* [StatusCake API Doc](https://statuscake.com/api/v1)
* [Comment automatiser le monitoring de nos 200 stacks clients en un déploiement ?](https://toucantoco.com/en/tech-blog/tech/ansible_monitoring)
* [How to automate the monitoring of our 200 customer stacks in one deployment?](https://toucantoco.com/en/tech-blog/tech/ansible_monitoring_en)
