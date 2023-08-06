![PyPI - Python Version](https://img.shields.io/pypi/pyversions/formal-sqlcommenter)

# Formal sqlcommenter

Python module for popular projects that want to add an external ID to your Formal logs.

 * [Psycopg2](#psycopg2)

## Local Install

```shell
pip3 install --user formal-sqlcommenter
```

## Usage

### Psycopg2

Use the provided cursor factory to generate database cursors. All queries executed with such cursors will have the SQL comment prepended to them.

```python
import psycopg2
from formal.sqlcommenter.psycopg2.extension import CommenterCursorFactory

cursor_factory = CommenterCursorFactory('1234')
conn = psycopg2.connect(..., cursor_factory=cursor_factory)
cursor = conn.cursor()
cursor.execute(...) # comment will be added before execution
```

which will produce a backend log such as when viewed on Postgresql
```shell
2019-05-28 02:33:25.287 PDT [57302] LOG:  statement: SELECT * FROM
polls_question *--formal_role_id: 1234 */
```

