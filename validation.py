from error import error


class Validator:
    def __init__(self):
        self.errors = []

    def check(self, string):
        if string != None and len(string) > 0:
            self.errors.append(string)

    def has_errors(self):
        return len(self.errors) > 0

    def __str__(self):
        message = ", ja ".join(self.errors)
        return message.capitalize()

    def not_empty(self, name, obj):
        if obj == None or (isinstance(obj, str) and len(obj) == 0):
            return f"{name} ei voi olla tyhjä"

    def has_length_more_than(self, name, string, length):
        if len(string) < length:
            return f"{name} ei voi olla lyhyempi kuin {length} kirjainta"

    def has_length_less_than(self, name, string, length):
        if len(string) > length:
            return f"{name} ei voi olla pidempi kuin {length} kirjainta"

    def is_value_between(self, name, num, minimum, maximum):
        if num.isdigit() and not (int(num) >= minimum and int(num) <= maximum):
            return f"{name} ei ole numero väliltä {minimum}-{maximum}"
