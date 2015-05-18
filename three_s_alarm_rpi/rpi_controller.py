import RPi.GPIO as GPIO
from pygame import mixer
from time import sleep
import os
import random


class RPiController:

    def __init__(self, led_gpio, servo_gpio, init_servo_value):
        self.led_gpio = led_gpio
        self.servo_gpio = servo_gpio
        GPIO.setmode(GPIO.BCM)
        self.clean_up_chanels()
	self.set_servoblaster_channel()

        if init_servo_value is not None:
            self.move_servo(init_servo_value)

    def clean_up_chanels(self):
        # clean up channel
        channel = self.led_gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.cleanup()

    def set_servoblaster_channel(self):
        """ 
        from /dev/servoblaster-cfg
        0 on P1-7           GPIO-4
        1 on P1-11          GPIO-17
        2 on P1-12          GPIO-18
        3 on P1-13          GPIO-27
        4 on P1-15          GPIO-22
        5 on P1-16          GPIO-23
        6 on P1-18          GPIO-24
        7 on P1-22          GPIO-25
        """
        gpio_blaster_map = {
            7: 0, 11: 1, 12: 2, 13: 3, 15: 4, 16: 5, 18: 6, 22: 7}
        if self.servo_gpio in gpio_blaster_map.keys():
            self.blaster_channel = gpio_blaster_map[self.servo_gpio]
        else:
            print('Not a valid GPIO pin for servo control (servoblaster)! ')

    def move_servo(self, position):
        servoStr = "%u=%u\n" % (self.blaster_channel, position)
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

    def play_setlist(self):
        while True:
            random_song = random.choice(self.list_songs)
            self.play_songfile(random_song)

    def play_songfile(self, song_file):
        mixer.init()
        mixer.music.load(song_file)
        mixer.music.play(1)
        while mixer.music.get_busy() == True:
            continue

    def set_playlist(self, song_folder):
        self.list_songs = [
            os.path.join(song_folder, fn) for fn in next(os.walk(song_folder))[2]]

        self.list_songs = [
            s for s in self.list_songs if '.mp3' in s or '.ogg' in s]
