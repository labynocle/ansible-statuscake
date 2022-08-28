# Ansible-statuscake

:warning: work in progress

This Ansible module setups/deletes a HTTP/TCP/PING test or a SSL certificate check via the [StatusCake](https://www.statuscake.com) API.

## Requirements

* Ansible >=2.1
* Python >=3.4

## Installation

Just copy the **library/status_cake_*.py** in your playbook folder

## status_cake_uptime :: Example usage:

...

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


## Links

* [StatusCake API Doc](https://statuscake.com/api/v1)
* [Comment automatiser le monitoring de nos 200 stacks clients en un déploiement ?](https://toucantoco.com/en/tech-blog/tech/ansible_monitoring)
* [How to automate the monitoring of our 200 customer stacks in one deployment?](https://toucantoco.com/en/tech-blog/tech/ansible_monitoring_en)
