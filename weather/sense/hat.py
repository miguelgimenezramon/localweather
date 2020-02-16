#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 10:17:38 2020

@author: gloppert
"""

from sense_emu import SenseHat
from threading import Thread
from time import sleep

class Measures:

    def __init__(self, temp, pressure, humidity):
        self.__temp = temp
        self.__pressure = pressure
        self.__humidity = humidity

    @property
    def temp(self):
        return self.__temp

    @temp.setter
    def temp(self, valor):
        self.__temp = valor

    @property
    def pressure(self):
        return self.__pressure

    @pressure.setter
    def pressure(self, valor):
        self.__pressure = valor

    @property
    def humidity(self):
        return self.__humidity

    @humidity.setter
    def humidity(self, valor):
        self.__humidity = valor


class Hat:

    OFFSET_LEFT = 0
    OFFSET_TOP = 0

    NUMS = [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1,  # 0
            0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,  # 1
            1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1,  # 2
            1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,  # 3
            1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1,  # 4
            1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1,  # 5
            1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1,  # 6
            1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0,  # 7
            1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,  # 8
            1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1]  # 9

    def __init__(self):
        self.__sensehat = SenseHat()
        self.__temp = True
        self.__contador = 0
        t = Thread(target=self.__start_weather_station)
        t.start()
        s = Thread(target=self.__start_capture_event)
        s.start()

    # Displays a single digit (0-9)
    def __show_digit(self, val, xd, yd, r, g, b):
        offset = val * 15
        for p in range(offset, offset + 15):
            xt = p % 3
            yt = (p - offset) // 3
            self.__sensehat.set_pixel(xt + xd, yt + yd, r * Hat.NUMS[p], g * Hat.NUMS[p], b * Hat.NUMS[p])


    # Displays a two-digits positive number (0-99)
    def __show_number(self, val, r, g, b):
        abs_val = abs(val)
        tens = abs_val // 10
        units = abs_val % 10
        if (abs_val > 9):
            self.__show_digit(tens, Hat.OFFSET_LEFT, Hat.OFFSET_TOP, r, g, b)
            self.__show_digit(units, Hat.OFFSET_LEFT + 4, Hat.OFFSET_TOP, r, g, b)

    def get_measures(self):
        measure = Measures(self.__sensehat.get_temperature(), self.__sensehat.get_pressure(), self.__sensehat.get_humidity())
        self.__contador += 1
        if self.__contador >= 30:
            self.__contador = 0
            # grabar temperaturas.
        return measure

    def __show_humidity(self, pressure):
        self.__sensehat.clear()
        self.__show_number(pressure,  47,119,255)
        self.__sensehat.set_pixel(0, 5, 255,255,255)
        self.__sensehat.set_pixel(0, 6, 255, 255, 255)
        self.__sensehat.set_pixel(0, 7, 255, 255, 255)
        self.__sensehat.set_pixel(1, 6, 255, 255, 255)
        self.__sensehat.set_pixel(2, 5, 255, 255, 255)
        self.__sensehat.set_pixel(2, 6, 255, 255, 255)
        self.__sensehat.set_pixel(2, 7, 255, 255, 255)

        self.__sensehat.set_pixel(4, 5, 255, 255, 255)
        self.__sensehat.set_pixel(4, 6, 255, 255, 255)
        self.__sensehat.set_pixel(4, 7, 255, 255, 255)
        self.__sensehat.set_pixel(5, 7, 255, 255, 255)
        self.__sensehat.set_pixel(6, 5, 255, 255, 255)
        self.__sensehat.set_pixel(6, 6, 255, 255, 255)
        self.__sensehat.set_pixel(6, 7, 255, 255, 255)

        self.__temp = False

    def __show_temp(self, temp):
        self.__sensehat.clear()
        self.__show_number(temp,  44,207,49)

        self.__sensehat.set_pixel(0, 5, 255,255,255)
        self.__sensehat.set_pixel(1, 5, 255, 255, 255)
        self.__sensehat.set_pixel(1, 6, 255, 255, 255)
        self.__sensehat.set_pixel(1, 7, 255, 255, 255)
        self.__sensehat.set_pixel(2, 5, 255, 255, 255)

        self.__sensehat.set_pixel(4, 5, 255, 255, 255)
        self.__sensehat.set_pixel(5, 5, 255, 255, 255)
        self.__sensehat.set_pixel(6, 5, 255, 255, 255)
        self.__sensehat.set_pixel(4, 6, 255, 255, 255)
        self.__sensehat.set_pixel(5, 6, 255, 255, 255)
        self.__sensehat.set_pixel(4, 7, 255, 255, 255)
        self.__sensehat.set_pixel(5, 7, 255, 255, 255)
        self.__sensehat.set_pixel(6, 7, 255, 255, 255)

        self.__temp = True

    def __start_weather_station(self):
        while True:
            measure = self.get_measures()
            self.__show_temp(int(measure.temp))
            sleep(15)
            self.__show_humidity(int(measure.humidity))
            sleep(15)

    def __start_capture_event(self):
        while True:
           for event in self.__sensehat.stick.get_events():
               if event.action == "pressed":
                   measure = self.get_measures()
                   if(not self.__temp):
                       self.__show_temp(int(measure.temp))
                   else:
                       self.__show_humidity(int(measure.humidity))
               sleep(0.5)








