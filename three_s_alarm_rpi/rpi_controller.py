import RPi.GPIO as GPIO
from pygame import mixer


class RPiController:

    def __init__(self, led_gpio, servo_gpio, init_servo_value):
        self.led_gpio = led_gpio
        self.servo_gpio = servo_gpio
        self.clean_up_chanels()

        if init_servo_value is not None:
            self.move_servo(init_servo_value)

    def clean_up_chanels(self):
        # clean up channel
        channel = self.led_gpio

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.cleanup()

        channel = self.servo_gpio

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.cleanup()

    def move_servo(self, position):
        servoStr = "%u=%u\n" % (self.servo_gpio, position)
        with open("/dev/servoblaster", "wb") as f:
            f.write(servoStr)

    def turn_on_LED(self, how_long=60 * 60 * 4):
        channel = self.led_gpio

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.HIGH)

    def turn_some_water(self, init_value, end_value):
        self.move_servo(init_value)
        self.move_servo(end_value)
        # channel = self.servo_gpio

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup

    def play_songfile(self, song_file):
        mixer.init()
        mixer.music.load(self.song_file)
        mixer.music.play(-1)
        while mixer.music.get_busy() == True:
            continue

    def set_playlist(self, song_folder):
        pass
