# -*- coding: utf-8 -*-
import re
import os
import locale

# To Do - enter docx files

locale.setlocale(locale.LC_ALL, 'English_United States')

location = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


class Unit(object):
    __metaclass__ = IterRegistry
    _registry = []


    def __init__(self, conversion, unit_dictionary):
        self._registry.append(self)
        self.num_regex = '(-)?(\d+(?:,+\d+)*)(\.\d+)?'
        self.conversion = conversion
        self.unit_dictionary = unit_dictionary


# LENGTH

inches = Unit(0.39370079, {"in": "cm", "inch": "centimeter", "inches": "centimeters"})
feet = Unit(3.28, {"feet": "meters", "ft": "m", "foot": "meters"})
yards = Unit(1.09361, {"yard": "meters", "yards": "meters", "yd": "m"})
miles = Unit(1.609344, {"miles": "kilometers", "mi": "km"})

# TEMPERATURE
temperature = Unit(9, {"°F": "°C", "degrees Fahrenheit": "degrees Celsius", "degrees F": "degrees C", "F": "C"})

# MASS
ounces = Unit(0.035274, {"ounces": "grams", "ounce": "grams", "oz": "g"})
pounds = Unit(2.20462, {"pounds": "kilograms", "pound": "kilogram", "lb": "kg"})
stones = Unit(0.157473, {"stones": "kilograms", "stone": "kilogram", "st": "kg"})

# AREA

sq_inch = Unit(0.157473, {"square inches": "square centimeters",
                          "square inch": "square centimeters", "sq in": "sq cm", "in²": "cm²"})
sq_feet = Unit(10.7639, {"square feet": "square meters", "sq ft": "sq m", "square foot": "square meters", "ft²": "m²"})
sq_yards = Unit(1.19599, {"square yards": "square meters",
                          "square yards": "square meters", "sq yd": "sq m", "yd²": "m²"})
sq_miles = Unit(0.386102, {"square miles": "square kilometers",
                           "square mile": "square kilometers", "sq mi": "sq km", "mi²": "km²"})
# VOLUME
pints = Unit(1.75975, {"pints": "litres", "pint": "litres", "pt": "l"})
quarts = Unit(0.879877, {"quarts": "litres", "quart": "litres", "gt": "l"})
gallons = Unit(0.219969, {"gallons": "litres", "gallon": "litres", "gal": "l"})


def convert_text(text, unit, i):

    regex = re.compile(unit.num_regex+'(\s)('+i+')\\b')
    return regex.findall(text)


def convert_value(text, unit):
    value_dict = {}

    for i in unit.unit_dictionary.keys():
        values = convert_text(text, unit, i)
        for p in values:
            american_value = ''.join(p)
            american_number = locale.atof(''.join(p[0:3]))
            american_unit = p[4]

            if american_unit in temperature.unit_dictionary.keys():
                european_number = str('{0:,}'.format(round((float(american_number - 32)) * 5 / unit.conversion, 2)))
            else:
                european_number = str('{0:,}'.format(round(float(american_number) / unit.conversion, 2)))

            european_unit = str(unit.unit_dictionary.get(american_unit))
            european_value = european_number + ' ' + european_unit
            value_dict[american_value] = european_value


    return value_dict


if __name__ == '__main__':
    obj_data = {}

    with open(os.path.join(location, 'text.txt'), 'r') as f:
        text = f.read()

        for obj in Unit._registry:
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
