import RPi.GPIO as GPIO


class PinManager(object):

    def __init__(self, pin_config):
        self.pin_config = pin_config
        self._initialize_gpio()
        self._initialize_pins()

    def _initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._gpio = GPIO

    def _initialize_pins(self):
        for item in self.pin_config:
            mode = self._gpio.__getattribute__(item['mode'])
            initial = self._gpio.__getattribute__(item.get('initial', 'LOW'))
            resistor = item.get('resistor', None)
            if resistor:
                resistor = self._gpio.__getattribute__(resistor)
                self._gpio.setup(item['pin'], mode, initial=initial, pull_up_down=resistor)
            else:
                self._gpio.setup(item['pin'], mode, initial=initial)
            # TODO: add event with handler function support

    def read(self, pin_number):
        return self._gpio.input(pin_number)

    def write(self, pin_number, value):
        self._gpio.output(pin_number, value)

    def on(self, pin_number):
        return self.write(pin_number, 1)

    def off(self, pin_number):
        return self.write(pin_number, 0)

    def cleanup(self, pin_number=None):
        if pin_number:
            return self._gpio.cleanup(pin_number)
        return self._gpio.cleanup()
