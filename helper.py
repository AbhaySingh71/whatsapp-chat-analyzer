from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import plotly.express as px

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    # Get the top 15 most common emojis
    emoji_counts = Counter(emojis).most_common(15)
    emoji_df = pd.DataFrame(emoji_counts, columns=['emoji', 'count'])

    return emoji_df

def visualize_emoji(data):
    emoji_df = pd.DataFrame(popular_emoji(data), columns=['emoji', 'count'])
    
    fig = px.pie(emoji_df, values='count', names='emoji', color_discrete_map="identity", title='Emoji Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def popular_emoji(data):
    total_emojis_list = list([a for b in data.emoji for a in b])
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_list = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    return emoji_list

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    user_heatmap = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)

    if selected_user == 'Overall':
        user_heatmap = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)

    # Create a Plotly heatmap figure
    fig = px.imshow(user_heatmap, labels=dict(x='Period', y='Day', color='Message Count'),
                    x=user_heatmap.columns, y=user_heatmap.index,color_continuous_scale='blackbody')
    fig.update_xaxes(title_text='Period')
    fig.update_yaxes(title_text='Day')
    fig.update_layout(title='Activity Heatmap')
    
    return fig


def day_wise_count(data):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    day_df = pd.DataFrame(data["message"])
    day_df['day_of_date'] = data['date'].dt.weekday
    day_df['day_of_date'] = day_df["day_of_date"].apply(lambda d: days[d])
    day_df["messagecount"] = 1
    
    day = day_df.groupby("day_of_date").sum()
    day.reset_index(inplace=True)
    
    fig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            )),
        showlegend=False
    )
    
    return fig