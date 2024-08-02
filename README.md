# Olympics Eagle

Really scrappy selenium bot to monitor ticket availability on Paris Olympics 2024 resale platform.

Tracks state of availability and sends a notification via the Pushover app when new tickets are released.


## Setup

Install the project

```
poetry install
pre-commit install
```

Use these excellent instructions to setup selenium with chrome driver on ubuntu.

https://github.com/password123456/setup-selenium-with-chrome-driver-on-ubuntu_debian

Ensure that valid keys are present in the pushover_api_keys.json file for the Pushover app. This will require setting up an application in Pushover.

Run the program by executing

```
python src/main.py
```
Alternatively, execute in extremely verbose debug mode

```
python src/main.py --debug
```

## Todo

- Unit tests once self respect is found
