# ezdatabase
## Making Databases easier

EzDatabase is a simple Database Wrapper for Python! Inspired by Repl.it Database!

## Features

- Works with a Key / Value System
- Can store strings, numbers, objects, booleans

## Code Examples

- Initialize Database
#
#
```python
from ezdatabase import db

database = db("MyDatabase.db")
# Returns None
```

- Set / Update Value of a Key
#
#
```python
# Arguments: key_name, key_value
database["User1"] = {"age": 10, "name": "John"})
database["Product: 21398"] =  "10,30 EUR"
# Returns True on Success
```

- Read the Value of a Key
#
#
```python
value = database["User1"]
# Returns the Value of a Key
```
- Delete a Key
#
#
```python
del database["User1"]
# Returns True on Successful removal of the Key
```