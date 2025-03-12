# import serializer from rest_framework
from rest_framework import serializers

class Geeks(object):
    def __init__(self, choices, multiplechoices):
        self.choices = choices
        self.multiplechoices = multiplechoices

    # create a tuple
GEEKS_CHOICES =(
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)


# create a serializer
class GeeksSerializer(serializers.Serializer):
    # initialize fields
    choices = serializers.ChoiceField(
        choices=GEEKS_CHOICES)
    multiplechoices = serializers.MultipleChoiceField(
        choices=GEEKS_CHOICES)
