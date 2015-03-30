import yaml
import sched
import time
import rpi_controller
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
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.Rpi = rpi_controller.RPiController(self.settings['led_settings']['gpio_led'], self.settings[
                                                'water_settings']['gpio_servo'], self.settings['water_settings']['init_value'])

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
        if self.settings['turn_on_led']:
            self.Rpi.turn_on_LED()
        # if self.settings['play_songs']:
            # self.Rpi.play_songfile()

        # put the sched to execture the water (ir required),
        # to give a change for you to wakeup
        if self.settings['turn_some_water']:
            ivalue = self.settings['water_settings']['init_value']
            evalue = self.settings['water_settings']['end_value']
            self.schedule.enter(self.settings['water_settings'][
                'chance_time'] * 60, 1, self.Rpi.turn_some_water, (ivalue, evalue))

    def activate(self):
        print('Waiting for wakeup hour...')
        self.schedule = sched.scheduler(time.time, time.sleep)

        FMT = '%H:%M'
        pprint(self.settings)
        tdelta = datetime.strptime(self.settings['hour'], FMT) - time_now()
        seconds2wait = tdelta.total_seconds()

        if seconds2wait < 0:  # go to next day
            seconds2wait = seconds2wait + 24 * 60 * 60

        self.schedule.enter(seconds2wait, 1, self.wakeup, ())
        self.schedule.run()
