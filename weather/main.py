#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 19:12:24 2020

@author: gloppert
"""

# -*- coding: utf-8 -*-


from weather.sense.hat import Hat


def main():
    hat = Hat()
    skill = hat.get_measures()

    print(f'La temperatura actual es: {skill.temp}')
    print(f'La humedad actual es: {skill.humidity}')
    print(f'La pression barometrica es: {skill.pressure}')


if __name__ == '__main__':
    main()