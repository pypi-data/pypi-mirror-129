# OSC OpenAPI Framework
Build and parse OpenAPI data using its own structured python object.

## Features
  - Build OpenAPI data from structured object
  - Parse OpenAPI data to structured object



## Installation

You can install the pre-built python package through this command:

```bash
$ pip install osc-openapi-framework
```

## Building

To build the package yourself:

```bash
$ make package
```

You can then install it with:
```bash
$ pip install dist/osc_openapi_framework-*.whl
```

## Usage
### Parsing OpenAPI Data
```python
from osc_openapi_framework.openapi.parser import parse as openapi_parse

openapi_data = '''
    openapi: 3.0.0
    info:
      title: Sample API
      description: Optional multiline or single-line description in [CommonMark](http://commonmark.org/help/) or HTML.
      version: 0.1.9
    security:
      - ApiKeyAuth: []
    servers:
      - url: http://api.example.com/v1
        description: Optional server description, e.g. Main (production) server
      - url: http://staging-api.example.com
        description: Optional server description, e.g. Internal staging server for testing
    paths:
      /users:
        get:
          summary: Returns a list of users.
          description: Optional extended description in CommonMark or HTML.
          responses:
            '200':    # status code
              description: A JSON array of user names
              content:
                application/json:
                  schema: 
                    type: array
                    items: 
                      type: string
'''
with open('/tmp/openapi_test', 'w') as fd:
  fd.write(openapi_data)
oapi = openapi_parse('/tmp/openapi_test')
```

## License

> Copyright Outscale SAS
>
> BSD-3-Clause

This project is compliant with [REUSE](https://reuse.software/).
