
# Web application for identifying completed forms

#### How the application works:

- The application receives 4 types of data as input;
- Compares these data types in the validator with names + checks their correctness;
- Based on the names, it is compared with templates from the database;
- If there is a template, we return the name of the template / If there is no template, we return the field types.

#### Stack:

Python 3.11 | Flask 3.0 | TinyDB 4.8 | pytest 7.4.3

## Installation

#### Cloning the repository
```
  git clome git@github.com:Anstane/web_form_matcher.git
```

#### Go to the application folder
```
  cd web_form_matcher/
```

#### Launch docker compose
```
  docker compose up
```
## Reference requests

#### POST request receiving the template name in response

```
  POST /get_form
```

```json
{
    "f_name_1": "test@test.ru",
    "f_name_2": "+79101112233"
}
```

#### POST request returning field types

```
  POST /get_form
```

```json
{
    "f_name_1": "another random text",
    "f_name_2": "random text"
}
```



## Running tests manually

```
  docker-compose exec app poetry run pytest -v
```


## Author

- [Mikhail Moskovkin](https://github.com/Anstane)

