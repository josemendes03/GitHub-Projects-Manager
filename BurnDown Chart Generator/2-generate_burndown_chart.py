import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read the data from the CSV file
dates = []
open_issues = []
date_issues = {}  # Dictionary to track open issue counts per day

# Open the CSV file and process the data
with open('issues_data.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # Parse the dates with timezone
        created_at = datetime.strptime(row['created_at'], "%Y-%m-%d %H:%M:%S%z")
        closed_at = None
        if row['closed_at']:
            closed_at = datetime.strptime(row['closed_at'], "%Y-%m-%d %H:%M:%S%z")
        
        # Update open count: Increment for "open", decrement for "closed"
        date_str_created = created_at.strftime('%Y-%m-%d')
        if date_str_created not in date_issues:
            date_issues[date_str_created] = 0
        date_issues[date_str_created] += 1
        
        if closed_at:
            date_str_closed = closed_at.strftime('%Y-%m-%d')
            if date_str_closed not in date_issues:
                date_issues[date_str_closed] = 0
            date_issues[date_str_closed] -= 1

# Ensure no negative values and accumulate open issues over time
sorted_dates = sorted(date_issues.keys())
open_count = 0
for date_str in sorted_dates:
    open_count += date_issues[date_str]
    open_count = max(open_count, 0)  # Ensure open_count is never negative
    date_issues[date_str] = open_count

# Prepare data for plotting
for date_str, count in sorted(date_issues.items()):
    dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
    open_issues.append(count)

# Plot the burndown chart
plt.figure(figsize=(10, 5))
plt.plot(dates, open_issues, marker='o', linestyle='-', color='b')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.gcf().autofmt_xdate()
plt.xlabel('Date')
plt.ylabel('Open Issues')
plt.title('Burndown Chart')
plt.grid(True)
plt.show()