# Prerequisites

Set following variables to make API work

```
export POSTGRESQL_HOST=<<redacted>>
export POSTGRESQL_USER=<<redacted>>
export POSTGRESQL_PASSWORD=<<redacted>>
export POSTGRESQL_DATABASE=<<redacted>>
export POSTGRESQL_PORT=<<redacted>>
```

# Python virtual env - optional


### create
`python3 -m venv fastapi`

### activate
`source fastapi/bin/activate`


# Python packages

- fastapi
- pydantic
- uvicorn
- os
- sqlalchemy
- psycopg2

`pip3 install fastapi pydantic uvicorn psycopg-binary sqlalchemy`


# Uvicorn

To start local server 

`uvicorn main:app --reload`

