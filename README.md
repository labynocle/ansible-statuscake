# Ansible-statuscake

This ansible module setups/deletes a HTTP/TCP/PING test via [StatusCake](https://www.statuscake.com) API. 

## Requirements

Ansible >=2.1

## Installation

Just copy the **library/status_cake_test.py** in your playbook folder

## Example usage:

```
- hosts: localhost
  vars_files:
    - "dict_example.yml"

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
        user_agent:      "Status Cake Monitoring"             # Use to populate the test with a custom user agent
        status_codes:    "200,204,205"                        # Comma seperated list of statusCodes to trigger error
        node_locations:  "AU1,AU5,AU3"                        # Any test locations seperated by a comma (using the Node Location IDs)
        follow_redirect: 1                                    # Use to specify whether redirects should be followed, set to 1 to enable
        contact:         "1234,42"                            # Contact group ID assoicated with account to use. Comma separation for multiple IDs.
      with_dict: "{{ example }}"
```

## Links

* [StatusCake API Doc](https://www.statuscake.com/api/Tests/Updating%20Inserting%20and%20Deleting%20Tests.md)

## TODO
* Role for Ansible galaxy
* Edge cases
