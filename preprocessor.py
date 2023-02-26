import pandas as pd
import re
import helper
import seaborn as sns


def preprocess(data):
    ptrn = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}\s(?:am|pm)\s-\s'
    msgs = re.split(ptrn, data)[1:]
    dates = re.findall(ptrn, data)

    df = pd.DataFrame({'user_msgs' : msgs, 'msgs_dates' : dates})
    #CONVERTING MESSAGE DATE TYPE TO DATE-TIME...
    df['msgs_dates'].str.replace('pm','PM').str.replace('am','AM')
    df['msgs_dates'] = pd.to_datetime(df['msgs_dates'], format = '%d/%m/%y, %I:%M %p - ')
    
    users = []
    messages = []

    for message in df['user_msgs']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:#user names
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df1 = df[['msgs_dates', 'user', 'message']]
    df1['year'] = df1['msgs_dates'].dt.year
    df1['month'] = df1['msgs_dates'].dt.month_name()
    df1['day'] = df1['msgs_dates'].dt.day
    df1['hour'] = df1['msgs_dates'].dt.hour
    df1['minute'] = df1['msgs_dates'].dt.minute
    df1['date'] = df1['msgs_dates']
    df1['day_name'] = df1['msgs_dates'].dt.day_name()
    df1['month_num'] = df1['msgs_dates'].dt.month
    

    period = []
    for hour in df1[['day_name', 'hour', ]]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df1['period'] = period

    df2 = df1[['date' , 'user', 'message', 'year', 'month', 'day', 'hour', 'minute','day_name','month_num', 'period']]
    return df2

    