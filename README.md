# Storehouse

Storehouse is a centralized threat intelligence list and indicator management tool for importing indicators of compromise into memcached for enrichment in Logstash, as well as APIs for external system interaction

> :warning: **This is a work in progress**

# Get Started

```
pipenv install
pipenv run python storehouse.py
```



# Roadmap

- [x] Support for externally hosted lists
- [ ] Support for lists behind API keys
- [ ] Support for custom lists
- [ ] Support for additional list types (e.g. hashes, filenames, custom)
- [ ] UI for managing lists

# Screenshot

![storehouse.gif](storehouse.gif)

# Setup

## Install

```
git clone https://github.com/n3tsurge/storehouse.git
cd storehouse
pipenv install
pipenv run python storehouse.py
```

## Editing Lists

1. Open lists.json
2. Add/Modify lists in the file
3. Save the file
4. Restart storehouse

### Defining Lists

```
[
    {
        "name": "SpamHaus Drop",
        "url": "https://www.spamhaus.org/drop/drop.txt",
        "format": "cidr",
        "refresh_interval": 60,
        "disabled": true,
        "type": "list"
    },
    {
        "name": "SpamHaus eDrop",
        "url": "https://www.spamhaus.org/drop/edrop.txt",
        "format": "cidr",
        "refresh_interval": 60,
        "disabled": true,
        "type": "list"
    },
    {
        "name": "Emerging Threats",
        "url": "http://rules.emergingthreats.net/blockrules/compromised-ips.txt",
        "format": "ip",
        "disabled": false,
        "type": "list"
    }
]
```