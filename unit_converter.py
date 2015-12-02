# -*- coding: utf-8 -*-
import re

#TO DO - set locale

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

list_of_objects = [inches, feet, miles, temperature, yards] #TO DO - iterate through class???

def convert_text():

    with open('C:\\Users\\Macek\\PycharmProjects\\American to normal\\text.txt', 'r') as input:
        text = input.read()

        value_dict = {} # matches imperial values with metric values

        def convert_value(obj):
            for i in obj.unit_dictionary.keys():
                regex = re.compile(obj.num_regex+'(\s)('+i+')\\b')
                values = regex.findall(text)
                for p in values:
                    american_value = ''.join(p)
                    american_number = float(''.join(p[0:3]))
                    american_unit = p[4]
                    if american_unit in temperature.unit_dictionary.keys():
                        european_number = str(round((float(american_number - 32)) * 5 / obj.conversion, 2))
                    else:
                        european_number = str(round(float(american_number) / obj.conversion, 2))
                    european_unit = str(obj.unit_dictionary.get(american_unit))
                    european_value = european_number + ' ' + european_unit
                    value_dict[american_value] = european_value

        for j in list_of_objects:
            convert_value(j)


    with open('C:\\Users\\Macek\\PycharmProjects\\American to normal\\output.txt', 'w') as output:
        if not value_dict:
            output.write(text)
        else:
            pattern = re.compile(r'|'.join(value_dict.keys()))
            output.write(pattern.sub(lambda x: value_dict[x.group()], text))

convert_text()