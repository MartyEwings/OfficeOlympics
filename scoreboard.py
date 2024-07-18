from flask import Flask, render_template_string
import pandas as pd
import threading
import time

app = Flask(__name__)

CSV_FILE = 'scores.csv'
REFRESH_INTERVAL = 300  # 5 minutes in seconds

# HTML template for the scoreboard
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Office Olympics Scoreboard</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f4f9;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .container {
      width: 80%;
      margin: auto;
      background: white;
      padding: 20px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
      text-align: center;
    }
    h1 {
      color: #333;
      margin-bottom: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: auto;
    }
    th, td {
      border: 1px solid #ddd;
      padding: 12px;
      text-align: center;
    }
    th {
      background-color: #4CAF50;
      color: white;
    }
    tr:nth-child(even) {
      background-color: #f2f2f2;
    }
    tr:hover {
      background-color: #ddd;
    }
    .gold {
      background-color: #FFD700 !important;
      color: #333 !important;
      font-weight: bold;
    }
    .silver {
      background-color: #C0C0C0 !important;
      color: #333 !important;
      font-weight: bold;
    }
    .bronze {
      background-color: #CD7F32 !important;
      color: #333 !important;
      font-weight: bold;
    }
    .icon {
      font-size: 1.2em;
    }
    .refresh-note {
      text-align: center;
      color: #777;
      margin-top: 10px;
    }
    .olympic-rings {
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="olympic-rings">
      <svg width="200" height="100" viewBox="0 0 300 150">
        <circle cx="50" cy="50" r="40" stroke="blue" stroke-width="10" fill="none"/>
        <circle cx="150" cy="50" r="40" stroke="black" stroke-width="10" fill="none"/>
        <circle cx="250" cy="50" r="40" stroke="red" stroke-width="10" fill="none"/>
        <circle cx="100" cy="100" r="40" stroke="yellow" stroke-width="10" fill="none"/>
        <circle cx="200" cy="100" r="40" stroke="green" stroke-width="10" fill="none"/>
      </svg>
    </div>
    <h1><i class="fas fa-trophy"></i> Office Olympics Scoreboard</h1>
    <table>
      <thead>
        <tr>
          <th>Team Name</th>
          {% for event in events %}
          <th>{{ event }}</th>
          {% endfor %}
          <th>Total Score</th>
        </tr>
      </thead>
      <tbody>
        {% for team in teams %}
        <tr class="{{ team['class'] }}">
          <td>{{ team['name'] }}</td>
          {% for score in team['scores'] %}
          <td>{{ score }}</td>
          {% endfor %}
          <td>{{ team['total'] }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    <p class="refresh-note">Page refreshes every 5 minutes to update scores</p>
  </div>
  <script>
    setTimeout(function() {
      window.location.reload(1);
    }, {{ refresh_interval }});
  </script>
</body>
</html>
'''

# Function to read scores from CSV file and calculate totals
def read_scores():
    df = pd.read_csv(CSV_FILE)
    df['Total'] = df.iloc[:, 1:].sum(axis=1)
    df = df.sort_values(by='Total', ascending=False)
    
    teams = []
    for index, row in df.iterrows():
        team_class = ''
        if index == 0:
            team_class = 'gold'
        elif index == 1:
            team_class = 'silver'
        elif index == 2:
            team_class = 'bronze'
        teams.append({
            'name': row[0],
            'scores': row[1:-1].tolist(),
            'total': row['Total'],
            'class': team_class
        })
    
    events = df.columns[1:-1].tolist()
    return teams, events

# Endpoint to serve the scoreboard
@app.route('/')
def scoreboard():
    teams, events = read_scores()
    return render_template_string(HTML_TEMPLATE, teams=teams, events=events, refresh_interval=REFRESH_INTERVAL * 1000)

# Function to periodically refresh the scores
def refresh_scores():
    while True:
        read_scores()
        time.sleep(REFRESH_INTERVAL)

if __name__ == '__main__':
    # Start the thread to refresh scores
    refresh_thread = threading.Thread(target=refresh_scores)
    refresh_thread.daemon = True
    refresh_thread.start()
    
    # Run the Flask web server
    app.run(debug=True)

