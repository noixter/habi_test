# HABI TEST

Microservice to search available real estate and rating them based on its
characteristics

## Related Technologies

- Python 3.10.4
  - mysql python lib

## General Questions
- how to check PEP8 or any linter over python? use pre-commit? or CI/CD?
- Use of starlette for http requests?, or use **python requests library** instead?

## Search Service

Microservice to filtered search about available properties, service can list
both sold or for sale properties based on determinate filters

#### Filters
- status:
  - pre_venta
  - en_venta
  - vendido

#### Properties Info
- Address
- City
- State
- Sale price
- Description

### Questions
- Use a simple MVC patter or try to implement a little version of CQRS?
- Define an access db strategy (design pattern or little ORM implementations)
  - how to construct a db connector?, define a strategy to make queries through only python
- how to handle http request without a framework?, do I use a microframework or maybe implement
  a http service based on some python core library? (eg. http, requests, etc.)
  - which design pattern to implement view over http implementation? (decorator to handled filters?)