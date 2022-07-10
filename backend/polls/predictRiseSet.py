import math
from datetime import date
import datetime as dt

class PredictRiseSet:
    def __init__(self, date, latitude, longitude, standard):
        self.year = int(date[0:4])
        self.month = int(date[4:6])
        self.day = int(date[6:8])
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.standard = float(standard)
    
    def calculate(self):
        baseDate = date(self.year, 1, 1)

        inputDate = date(self.year, self.month, self.day)
        daysNum = (inputDate - baseDate).days

        delta = math.radians(-23.5 * math.cos(math.radians(360/365*(daysNum+10))))
        theta = math.radians(self.latitude)
        a = math.radians(-0.83)

        w = math.acos((math.sin(a) - (math.sin(delta) * math.sin(theta))) / (math.cos(delta) * math.cos(theta)))
        w = math.degrees(w)

        standard_longitude = self.standard*15
        longitudeDiff = int((standard_longitude-self.longitude)/15*60)

        setHour = int(w // 15) + 12
        setMinute = round(w % 15 / 15 * 60)
        setTime = dt.timedelta(hours=setHour, minutes=setMinute) + dt.timedelta(minutes=longitudeDiff)

        riseHour = int(24 - (setHour+setMinute/60))
        riseMinute = round((24 - (setHour+setMinute/60) - riseHour)*60)
        riseTime = dt.timedelta(hours=riseHour, minutes=riseMinute) + dt.timedelta(minutes=longitudeDiff)

        return str(riseTime), str(setTime)