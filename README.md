# Desktop testing project

## Description

A project for testing ONLYOFFICE Desktop.

## Requirements

* Python 3.6 or newer

## Installing Python Libraries

* Create virtual environment

`python3 -m venv venv`

* activate virtual environment

`source ./venv/bin/activate`

* install requirements

`python3 install_requirements.py`

## Sending messages to Telegram

* To send test reports to Telegram,
you need to add two files to the `~/.telegram` directory:
  * `token` file containing the bot token
  * `chat` file with chat ID

## Getting Started

* activate virtual environment

`source ./venv/bin/activate`

### Command for starting desktop open test

`invoke open-test -v <version>`

#### Flags open-test command

`-v <version>` or `--version <version>` - specifies a testing version

`-d` or `--display` - to run tests in virtual display

`-c <path to custom config.json>` or `--config <path to custom config.json>` -
to specify a custom configuration file

`-t` or `--telegram` - to send the report to telegram

`-l` or `--license` - to specify the license file

#### Example open-test command

`invoke open-test -d -t -v 7.4.1.36 -c ./my_config.json`

### Command for install desktop

`invoke install-desktop -v <version>`

#### Flags install-desktop command

`-v <version>` or `--version <version>` - specifies a testing version

`-c <path to custom config.json>` or `--config <path to custom config.json>` -
to specify a custom configuration file

`-t` or `--telegram` - to send the report to telegram

`-l` or `--license` - to specify the license file

#### Example install-desktop command

`invoke install-desktop -t -v 7.4.1.36 -c ./my_config.json`
