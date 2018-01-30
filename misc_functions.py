# Extra functionality
"""
The following function helps change the cursor's results into useable
SQL that the html templates can read.
"""
from django.utils import timezone
from django.conf import settings
import datetime, pytz

from collections import namedtuple
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]


def convert_extracted_time(datetime):
    """
    NearBeach stores its time in UTC. This function is designed to get the UTC time and convert it into
    the correct timezone, and from there it then converts the time into a dictionary model (hour, minutes, AM/PM)
    and returns that.
    :param datetime: this will be the datetime extract from the model
    :return: { 'hour': hour, 'minute': minute, 'meridiem': meridiem }
    """
    datetime = datetime.replace(tzinfo=pytz.utc) #Make sure Django knows its in UTC time
    datetime_converted = datetime.astimezone(pytz.timezone(settings.TIME_ZONE))

    #Extract into variables to manipulate into NearBeach format
    year = datetime_converted.year
    month = datetime_converted.month
    day =datetime_converted.day
    hour = datetime_converted.hour
    minute = datetime_converted.minute

    """
    The 24 hours to 12 hours formula.
    00:00 means that it is 12:00 AM - change required for hour
    01:00 means that it is 01:00 AM - no change required
    12:00 means that it is 12:00 PM - change required for meridiem
    13:00 means that it is 01:00 PM - change required for hour and meridiem
    """
    meridiem = u'AM'
    if hour == 0:
        hour = 12
    elif hour == 12:
        meridiem = u'PM'
    elif hour > 12:
        hour = hour - 12
        meridiem = u'PM'

    #Time to return the dictionary
    return {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'meridiem': meridiem,
    }


def convert_to_utc(year, month, day, hour, minute, meridiem):
    """
    The data from the form is inputted into this function. The time is then converted into UTC from the local timezone.
    From there the datetime of the UTC is returned for input into the database.
    :param datetime:
    :return:
    """

    #Convert the hour:meridiem into 24-H
    if meridiem == "AM":
        if hour == 12:
            hour = 0
    else:
        if hour < 12:
            hour = hour + 12

    location = pytz.timezone(settings.TIME_ZONE)
    local_time = location.localize(datetime.datetime(year, month, day, hour, minute))

    return local_time.astimezone(pytz.utc)
