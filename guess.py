from datetime import datetime, timedelta, time

from pytz import timezone

midday = time(12)

import astropy.coordinates as coord
from astropy.time import Time

import config

tz=timezone(config.tz)

def time2altitude(time: datetime) -> float:
    astro_time = Time(tz.localize(time))
    altaz = coord.AltAz(location=config.loc, obstime=astro_time)
    sun = coord.get_sun(astro_time)
    return sun.transform_to(altaz).alt.degree


def get_time(altitude, time=False):
    lower = datetime.combine(datetime.now().date(), midday)
    upper = lower + timedelta(hours=12)

    while upper - lower > timedelta(seconds=30):
        middle = lower + (upper - lower) / 2
        if time2altitude(middle) > altitude:
            lower = middle
        else:
            upper = middle
        # print(upper, lower)

    return lower + (upper - lower) / 2


if __name__ == "__main__":
    target = 14.480046611643763
    print(get_time(target))
