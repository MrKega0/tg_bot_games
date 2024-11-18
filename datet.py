import datetime
import pytz

print(datetime.datetime.now())
time_now = datetime.datetime.now(tz=pytz.timezone('Europe/Paris'))
time_now_m = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
print(time_now_m-time_now)
print(time_now)

time_future = datetime.datetime(year=2024, month=12,day=10, tzinfo=pytz.timezone('Europe/Moscow'))
print(time_future)

print(time_future-time_now)

td = datetime.timedelta(minutes=1)

print(time_now + td)

# print(pytz.all_timezones)