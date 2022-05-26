# Ruuvi Greengrass Component

Ruuvi Greengrass component is a component you can install to AWS GreenGrass device to relay measurements received from your RuuviTags to an MQTT topic and/or IoT Core endpoint.

https://docs.aws.amazon.com/greengrass/v2/developerguide/what-is-iot-greengrass.html

## Installation

Install GreenGrassCore by instructions in: https://docs.aws.amazon.com/greengrass/v2/developerguide/quick-installation.html

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-development-kit-cli.html

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Setting up development environment

Recommending to use virtual environments for developing on your local environment: https://realpython.com/intro-to-pyenv/

**First create a virtual env:**
> pyenv virtualenv 3.10.3 ruuvi-gg-component

**Activate the environment in the project folder:**
> pyenv local ruuvi-gg-component

### Using a public MQTT Test broker
test.mosquitto.org

### Sending test msgs
mosquitto_pub -h test.mosquitto.org -m "test" -t /ruuvi/abc1234/temperature
mosquitto_sub -h test.mosquitto.org -t /ruuvi/#


## License
[MIT](https://choosealicense.com/licenses/mit/)