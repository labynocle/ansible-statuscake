# Ansible-statuscake

This Ansible module setups/deletes a HTTP/TCP/PING test via [StatusCake](https://www.statuscake.com) API. 

## Requirements

Ansible >=2.1

## Installation

Just copy the **library/status_cake_test.py** in your playbook folder

## Example usage:

```
- hosts:      localhost
  vars_files: "dict_example.yml"

  tasks:
    - name: Create StatusCake test
      status_cake_test:
        username:        "example_user"                       # StatusCake login name
        api_key:         "som3thing1se3cret"                  # StatusCake API key (cf: https://app.statuscake.com/APIKey.php)
        state:           "present"                            # If present the task will try to create/update the test, if absent the task will delete the test
        name:            "{{ item.value.url }}"               # Website name
        url:             "{{ item.value.url }}"               # Test location, either an IP (for TCP and Ping) or a fully qualified URL
        test_tags:       "something,somethingelse,anotherone" # Tags should be seperated by a comma
        test_type:       "HTTP"                               # What type of test type to use (HTTP/TCP/PING)
        check_rate:      300                                  # The number of seconds between checks
        trigger_rate:    5                                    # How many minutes to wait before sending an alert
        confirmation:    5                                    # How many different servers are needed to confirm the downtime
        user_agent:      "Status Cake Monitoring"             # Use to populate the test with a custom user agent
        custom_header:                                        # Custom HTTP header, must be dict which will be sent as a JSON to StatusCake
          Header01: Plop
          Header02: Plip
        status_codes:    "200,204,205"                        # Comma seperated list of statusCodes to trigger error
        node_locations:  "AU1,AU5,AU3"                        # Any test locations seperated by a comma (using the Node Location IDs)
        follow_redirect: 1                                    # Use to specify whether redirects should be followed, set to 1 to enable
        contact:         "1234,42"                            # Contact group ID assoicated with account to use. Comma separation for multiple IDs.
        #find_string:    "plop"                               # A string that should either be found or not found.
        #do_not_find:    0                                    # If the above string should be found to trigger a alert. 1 = will trigger if FindString found
      with_dict:         "{{ example }}"
```


## Tips / Dirty quick win

### How to use `post_raw` with a JSON

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


## ToDo and ideas

- [ ] Role for Ansible galaxy
- [ ] Edge cases
- [ ] Add tests on some configurations and params (like json for `custom_header`)
- [ ] [Manage SSL Tests](https://github.com/labynocle/ansible-statuscake/issues/5)


## Links

* [StatusCake API Doc](https://www.statuscake.com/api/Tests/Updating%20Inserting%20and%20Deleting%20Tests.md)
