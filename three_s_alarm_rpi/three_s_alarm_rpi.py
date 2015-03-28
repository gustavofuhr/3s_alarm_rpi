import yaml
import sched
import time
import three_s_alarm_rpi.rpi_controller
from datetime import datetime
from pprint import pprint


def time_now():
    d = datetime.now()
    stime = str(d.hour) + ":" + str(d.minute)
    FMT = '%H:%M'
    return datetime.strptime(stime, FMT)


class ThreeSAlarmRpi:

    def __init__(self, config_filename='./config.yaml'):
        self.read_config(config_filename)

        self.Rpi = rpi_controller.RPiController(self.settings['led_settings'][
                                                'gpio_led'], self.settings['servo_settings']['gpio_servo'])

    def read_config(self, config_filename):

        with open(config_filename) as stream:
            yconfig = yaml.load(stream)
            try:
                self.settings = yconfig['alarm_settings']

            except Exception as err:
                print('Problem reading the configuration file..')
                raise err

    def wakeup(self):
        print('Wake up pretty girl!')
        self.turn_on_LED()
        if self.play_song:
            self.play_songfile()

    def activate(self):
        print('Waiting for wakeup hour...')
        s = sched.scheduler(time.time, time.sleep)

        FMT = '%H:%M'
        pprint(self.settings)
        tdelta = datetime.strptime(self.settings['hour'], FMT) - time_now()
        seconds2wait = tdelta.total_seconds()

        if seconds2wait < 0:  # go to next day
            seconds2wait = seconds2wait + 24 * 60 * 60

        s.enter(seconds2wait, 1, self.wakeup, ())
        s.run()
