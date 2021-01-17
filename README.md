# Storehouse

Storehouse is a centralized threat intelligence list and indicator management tool for importing indicators of compromise into memcached for enrichment in Logstash, as well as APIs for external system interaction

# Get Started

```
pipenv install
pipenv run python storehouse.py
```

# Screenshot

![storehouse.gif](storehouse.gif)

# Defining Lists

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