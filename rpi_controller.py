import RPi.GPIO as GPIO
from pygame import mixer


class RPiController:

    def __init__(self, led_gpio, servo_gpio):
        self.led_gpio = led_gpio
        self.servo_gpio = servo_gpio
        self.clean_up_chanels()

    def clean_up_chanels(self):
        # clean up channel
        channel = self.led_gpio

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.cleanup()

        channel = self.gpio_servo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.cleanup()

    def turn_on_LED(self, how_long=60 * 60 * 4):
        channel = self.gpio_led

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.HIGH)

    def turn_some_water(self):
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
