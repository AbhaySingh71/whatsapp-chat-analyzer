import re  # Regular expressions for parsing data
import pandas as pd  # Pandas for data manipulation

def preprocess(data):
    """
    This function takes raw WhatsApp chat data as input and preprocesses it into a structured DataFrame.
    
    Args:
    - data: Raw chat data as a string.

    Returns:
    - df: A pandas DataFrame with processed chat data including user, message, date, time, and other extracted features.
    """
    
    # Define the pattern for identifying date and time in the chat data
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    # Split data into messages and extract dates
    messages = re.split(pattern, data)[1:]  # Extract messages by splitting based on the date pattern
    dates = re.findall(pattern, data)  # Extract all dates using the defined pattern

    # Create a DataFrame with 'user_message' and 'message_date' columns
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Convert 'message_date' to datetime format and rename to 'date'
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Initialize lists to store users and actual messages
    users = []
    messages = []

    # Loop through each message and split it into user and message content
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)  # Split each message into user and the actual message content
        
        if entry[1:]:  # If the message contains a username
            users.append(entry[1])  # Extract username
            messages.append(" ".join(entry[2:]))  # Extract the message content
        else:
            # If no username is found, it's likely a system message (group notification)
            users.append('group_notification')
            messages.append(entry[0])  # Extract the entire message as a system notification

    # Add 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column as it is now redundant
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date and time-related features from the 'date' column
    df['only_date'] = df['date'].dt.date  # Extract only the date
    df['year'] = df['date'].dt.year  # Extract the year
    df['month_num'] = df['date'].dt.month  # Extract the month number
    df['month'] = df['date'].dt.month_name()  # Extract the month name
    df['day'] = df['date'].dt.day  # Extract the day of the month
    df['day_name'] = df['date'].dt.day_name()  # Extract the day of the week
    df['hour'] = df['date'].dt.hour  # Extract the hour
    df['minute'] = df['date'].dt.minute  # Extract the minute

    # Create a new feature for message periods (e.g., "23-00" for messages sent at 23:xx hours)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))  # Special case for 23:xx to 00:xx
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))  # Special case for 00:xx to 01:xx
        else:
            period.append(str(hour) + "-" + str(hour + 1))  # General case for other hours

    # Add the 'period' feature to the DataFrame
    df['period'] = period

    # Return the processed DataFrame
    return df
