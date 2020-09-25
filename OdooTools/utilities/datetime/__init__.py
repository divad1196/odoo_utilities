import datetime
import pytz

def client_specific_to_utc(env, date):
    tz_name = env.context.get('tz') or env.user.tz
    if tz_name:
        tz = pytz.timezone(tz_name)
        local_date = tz.localize(date)
        date = local_date.astimezone(pytz.UTC).replace(tzinfo=None)
    return date
