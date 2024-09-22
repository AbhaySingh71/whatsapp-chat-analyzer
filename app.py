# Import necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import preprocessor, helper

# Title and description of the Streamlit app
st.title("WhatsApp Chat Analyzer 😃")
st.markdown("This app is used to analyze your WhatsApp Chat using the exported text file 📁.")

# Sidebar for user instructions and file upload
st.sidebar.image("banner.jpeg", use_column_width=True)  # Adding an image to the sidebar
st.sidebar.title("Analyze:")  # Sidebar title
st.sidebar.markdown("This app is used to analyze your WhatsApp Chat using the exported text file 📁.")
st.sidebar.markdown('**How to export chat text file?**')
st.sidebar.text('Follow the steps 👇:')
st.sidebar.text('1) Open the individual or group chat.')
st.sidebar.text('2) Tap options > More > Export chat.')
st.sidebar.text('3) Choose export without media.')

st.sidebar.markdown('*You are all set to go 😃*.')

# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read the uploaded file
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    # Preprocess the chat data
    df = preprocessor.preprocess(data)
    st.sidebar.markdown("**Don't worry your data is not stored!**")
    st.sidebar.markdown("**Feel free to use 😊.**")    
    
    # Extract unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")  # Add an option to show analysis for all users

    # Selectbox to choose which user's chat to analyze
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Show analysis when button is clicked
    if st.sidebar.button("Show Analysis"):
        
        # Fetch top statistics (total messages, words, media, links)
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        
        # Display top statistics in four columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly Timeline visualization
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig = px.line(timeline, x='time', y='message', title='Monthly Timeline', labels={'message': 'Messages'})
        st.plotly_chart(fig)

        # Daily Timeline visualization
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig = px.line(daily_timeline, x='only_date', y='message', title='Daily Timeline', labels={'message': 'Messages'})
        st.plotly_chart(fig)

        # Activity Map (Most Busy Day and Month)
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        # Most busy day
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig = px.bar(busy_day, x=busy_day.index, y=busy_day.values, title='Most Busy Day')
            st.plotly_chart(fig)

        # Most busy month
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig = px.bar(busy_month, x=busy_month.index, y=busy_month.values, title='Most Busy Month')
            st.plotly_chart(fig)

        # Weekly Activity Heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        st.plotly_chart(user_heatmap)

        # Day-wise count visualization (Polar Plot)
        st.title("Day-wise Message Count")
        day_wise_fig = helper.day_wise_count(df)
        st.plotly_chart(day_wise_fig)

        # Display most busy users if 'Overall' is selected
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig = px.bar(x, x=x.index, y=x.values, title='Most Busy Users')
            st.plotly_chart(fig)
            st.dataframe(new_df)

        # WordCloud visualization using Matplotlib
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')  # Hide axes
        st.pyplot(fig)

        # Most Common Words visualization
        most_common_df = helper.most_common_words(selected_user, df)
        most_common_df.columns = ['Word', 'Count']
        fig = px.bar(most_common_df, x='Word', y='Count', title='Most Common Words')
        st.plotly_chart(fig)

        # Emoji Analysis (Table + Chart)
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        # Display emoji data and visualization side by side
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig = helper.visualize_emoji(emoji_df)
            st.plotly_chart(fig)

        # Display complete data
        st.title("Complete DataFrame")
        st.dataframe(df)

# Footer badges and social media links
st.sidebar.markdown(
    "[![built with love](https://forthebadge.com/images/badges/built-with-love.svg)](https://www.linkedin.com/in/abhay-singh-050a5b293/)")
st.sidebar.markdown(
    "[![smile please](https://forthebadge.com/images/badges/makes-people-smile.svg)](https://x.com/@abhaysingh71711)")    
