from datetime import datetime
from statistics import mean, stdev

import astropy.coordinates as coord
from astropy.time import Time
from pytz import timezone

import config

loc = coord.EarthLocation(lon=config.lon,
                          lat=config.lat, height=config.height)
tz = timezone(config.tz)

with open("sonnenuntergang.txt") as f:
    content = f.readlines()
    lines = [line.strip() for line in content]

angles = []

for line in lines:
    if "#" in line or not line:
        continue
    parsetime = tz.localize(datetime.strptime("2018 " + line, "%Y %d.%m %H:%M"))
    print(parsetime.isoformat())
    time = Time(parsetime)
    print(time)
    altaz = coord.AltAz(location=loc, obstime=time)
    sun = coord.get_sun(time)

    altitude = sun.transform_to(altaz).alt.degree
    print(altitude)
    angles.append(altitude)

average = mean(angles)
stdev = stdev(angles, average)
print(stdev)

print(average)

with open("average.txt", "w") as f:
    f.write(str(average) + "\n" + str(stdev))
