import matplotlib.pyplot as plt
import pandas as pd
import datetime
# import preprocessor
import seaborn as sns



from urlextract import URLExtract
extractor = URLExtract()


def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # 1. FETCHING TOTAL NUMBER NUMBER OF MESSAGES:-
    num_messages = df.shape[0] 

    # 2. FETCHING TOTAL NUMBER OF WORDS:-
    words = [] 
    for message in df['message']:
        words.extend(message.split())

    # 3. FETCH NUMBER OF MEDIA MESSAGES:-
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. FETCH NUMBER OF LINKS 
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))


    return num_messages,len(words),num_media_messages,len(links)


def most_busy_user(df):
    x = df['user'].value_counts().head(7)        #maybe error...changed dataframe
    
    return x

def most_busy_user_pie(df):
    x1 = round((df['user'].value_counts().head(7)/df.shape[0])*100,2)
    return x1

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] +"-"+str(timeline['year'][i]))
    timeline['time'] = time
    return timeline



def weekly_activity(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['day_name'] = df['date'].dt.day_name()
    return df['day_name'].value_counts()


def monthly_activity(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()
  
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    activity_heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'message', aggfunc = 'count').fillna(0)

    return activity_heatmap