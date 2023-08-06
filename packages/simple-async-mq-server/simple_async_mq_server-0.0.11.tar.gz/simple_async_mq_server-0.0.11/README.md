# Simple Async Message Queue Server
### A simple implementation of an ESB / Kafka 
Implementation is done as part of a school project

## Server Example

```python
from simple_async_mq_server import server

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'siasmq'
}

server.start(port=10000, db_config=db_config)
```

## Currently supported transformations
Object and array definitions for each type can be found below.

| from / to   | JSON | XML | CSV | TSV |
|-------------|------|-----|-----|-----|
| JSON object |      |  ✅  |  ✅  |  🔜  |
| JSON array  |      |  🚫  |  ✅  |  🔜  |
| XML object  |   ✅  |     |  ✅  |  🔜  |
| XML array   |   ✅  |     |  ✅  |  🔜  |
| CSV object  |   ✅  |  ✅  |     |  🔜  |
| CSV array   |   ✅  |  🚫  |     |  🔜  |
| TSV object  |   🔜  |  🔜  |  🔜  |     |
| TSV array   |   🔜  |  🔜  |  🔜  |     |

## Object and array definitions
#### JSON object:
```json
{"person": 
  {"name": "john", "age": "20"}
}
```

#### JSON array:
```json
  [
    {"name": "john", "age": "20"},
    {"name": "john", "age": "20"}
  ]
```

#### XML object:
```xml
<?xml version="1.0" ?>
<person>
  <name>John Johnson</name>
  <age>20</age>
</person>
```
#### XML array:
```xml
<?xml version="1.0" ?>
<persons>
  <person>
    <name>Daryl Dixon</name>
    <age>33</age>
  </person>
  <person>
    <name>Rick Grimes</name>
    <age>35</age>
 </person>
</persons>
```
