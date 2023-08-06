# Kimiko Objects

A standard way for interacting with Kimiko Objects Services

## Instructions

1. Install

```
pip install kimiko_objects
```

2. Import Client

```
from kimiko_objects import Client
client = Client(<account_id>, <api_key>)
```

3. Use Kimko Objects

```
objects = client.objects()
records = client.records(<object_type>)
```
