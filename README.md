# Olympics Eagle

Monitor ticket availability on Paris 2024 resale platform and send a notification when new tickets are released.


## Setup

Install the project

```
poetry install
pre-commit install
```

Use these excellent instructions to setup selenium on ubuntu.

https://github.com/password123456/setup-selenium-with-chrome-driver-on-ubuntu_debian

Ensure that valid api keys are present in the pushover_api_keys.json file for the Pushover app.

Run the program by executing

```
python src/main.py
```
Alternatively

```
python src/main.py --debug
```

## Todo

tests??????
