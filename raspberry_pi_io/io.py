import yaml

from api import DeviceConfig
from gpio import PinManager
from rabbit import AsyncConsumer


class IOService(object):

    def __init__(self, config_file):
        with open(config_file) as file:
            self.config = yaml.safe_load(file)
        self.load_device_config()
        self.initialize_pin_manager()
        self.initialize_consumer()

    @staticmethod
    def _error(response):
        return {'error': 1, 'response': response}

    @staticmethod
    def _response(response):
        return {'error': 0, 'response': response}

    def load_device_config(self):
        self.device_config = DeviceConfig(
            api=self.config['api'],
            user_email=self.config['user_email'],
            user_key=self.config['user_key'],
            device_id=self.config['device_id']).get()

    def initialize_pin_manager(self):
        self.pin_manager = PinManager(self.device_config['pinConfig'])

    def initialize_consumer(self):

        def action(instruction):
            response = getattr(self.pin_manager, instruction['action'])(int(instruction['pin']))
            return {
                'response': response
            }

        self.consumer = AsyncConsumer(
            rabbit_url=self.device_config['rabbitURL'],
            queue=self.config['device_id'],
            exchange='raspberry-pi-io',
            exchange_type='direct',
            routing_key=self.config['device_id'],
            action=action)

    def start(self):
        try:
            self.consumer.run()
        except:
            self.consumer.stop()
            raise
