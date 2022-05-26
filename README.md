# Ruuvi Greengrass Component

Ruuvi Greengrass component is a component you can install to AWS GreenGrass device to relay measurements received from your RuuviTags to an MQTT topic and/or IoT Core endpoint.

https://docs.aws.amazon.com/greengrass/v2/developerguide/what-is-iot-greengrass.html

## Installation

Install GreenGrassCore by instructions in: https://docs.aws.amazon.com/greengrass/v2/developerguide/quick-installation.html



https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-development-kit-cli.html


Build component using GDK:
```bash
gdk component build
gdk component publish
```

In order to deploy these to Core devices, you must allow it to access S3 buckets:
https://docs.aws.amazon.com/greengrass/v2/developerguide/device-service-role.html#device-service-role-access-s3-bucket


## Usage


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Setting up development environment

Recommending to use virtual environments for developing on your local environment: https://realpython.com/intro-to-pyenv/

**First create a virtual env:**
```
pyenv virtualenv 3.10.3 ruuvi-gg-component
```

**Activate the environment in the project folder:**
```
pyenv local ruuvi-gg-component
```

**Install Greengrass Development Kit**
https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-development-kit-cli.html

```
python3 -m pip install -U git+https://github.com/aws-greengrass/aws-greengrass-gdk-cli.git@v1.1.0
```

**To run on the Greengrass device / Linux**
sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)


**Create S3 bucket for deployments**
```
aws s3 mb s3://vhartikainen-gg-deploybucket
```

### Using a public MQTT Test broker
test.mosquitto.org

### Sending test msgs
mosquitto_pub -h test.mosquitto.org -m "test" -t /ruuvi/abc1234/temperature
mosquitto_sub -h test.mosquitto.org -t /ruuvi/#

### Iterating
aws greengrassv2 delete-component \
              --arn arn:aws:greengrass:eu-west-1:374274434411:components:vhartikainen.RuuviTagSensor:versions:0.0.1

rm -r artifacts-unarchived/vhartikainen.RuuviTagSensor artifacts/vhartikainen.RuuviTagSensor

## License
[MIT](https://choosealicense.com/licenses/mit/)