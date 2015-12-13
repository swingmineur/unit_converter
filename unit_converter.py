# -*- coding: utf-8 -*-
import re
import os

# TO DO - set locale


location = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Unit(object):
    def __init__(self, conversion, unit_dictionary):
        self.num_regex = '(-)?(\d+)(\.\d+)?'
        self.conversion = conversion
        self.unit_dictionary = unit_dictionary

inches = Unit(0.39370079, {"in": "cm", "inch": "centimeter", "inches": "centimeters"})
feet = Unit(3.28, {"feet": "meters", "ft": "m", "foot": "meters"})
yards = Unit(1.09361, {"yard": "meters", "yards": "meters", "yd": "m"})
miles = Unit(1.609344, {"miles": "kilometers", "mi": "km"})
temperature = Unit(9, {"°F": "°C", "degrees Fahrenheit": "degrees Celsius", "degrees F": "degrees C", "F": "C"})


list_of_objects = [inches, feet, miles, temperature, yards]  # TO DO - iterate through class???


def convert_text(text, unit, i):

    regex = re.compile(unit.num_regex+'(\s)('+i+')\\b')
    return regex.findall(text)


def convert_value(text, unit):
    value_dict = {}

    for i in unit.unit_dictionary.keys():
        values = convert_text(text, unit, i)
        for p in values:
            american_value = ''.join(p)
            american_number = float(''.join(p[0:3]))
            american_unit = p[4]

            if american_unit in temperature.unit_dictionary.keys():
                european_number = str(round((float(american_number - 32)) * 5 / unit.conversion, 2))
            else:
                european_number = str(round(float(american_number) / unit.conversion, 2))

            european_unit = str(unit.unit_dictionary.get(american_unit))
            european_value = european_number + ' ' + european_unit
            value_dict[american_value] = european_value

    return value_dict


if __name__ == '__main__':
    obj_data = {}

    with open(os.path.join(location, 'text.txt'), 'r') as f:
        text = f.read()

        for obj in list_of_objects:
            obj_data[obj] = convert_value(text, obj)

    with open(os.path.join(location, 'output.txt'), 'w') as o:
        if not obj_data:
            o.write(text)
        else:
            units = {}
            for i in obj_data.values():
                units.update(i)
            pattern = re.compile(r'|'.join(units.keys()))
            o.write(pattern.sub(lambda x: units[x.group()], text))
