from datetime import datetime, timedelta, time

import astropy.coordinates as coord
from astropy.time import Time
from pytz import timezone

import config

midday = time(12)

tz = timezone(config.tz)


def time2altitude(time: datetime) -> float:
    astro_time = Time(tz.localize(time))
    altaz = coord.AltAz(location=config.loc, obstime=astro_time)
    sun = coord.get_sun(astro_time)
    return sun.transform_to(altaz).alt.degree


def get_time(altitude):
    lower = datetime.combine(datetime.now().date(), midday)
    upper = lower + timedelta(hours=12)

    while upper - lower > timedelta(seconds=1):
        middle = lower + (upper - lower) / 2
        if time2altitude(middle) > altitude:
            lower = middle
        else:
            upper = middle

    return lower + (upper - lower) / 2


if __name__ == "__main__":
    target = 14.480046611643763
    print(get_time(target))
