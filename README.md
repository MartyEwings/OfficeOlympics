# Office Olympics Scoreboard

This project is a simple web application to display a scoreboard for Office Olympics. The scoreboard displays team names, scores for various events, and total scores, with special highlighting for the top three teams. The scoreboard updates every 5 minutes to reflect any changes in the scores.

## Features

- Displays team names and scores for five events.
- Calculates and displays the total score for each team.
- Highlights the top three teams with gold, silver, and bronze colors.
- Automatically refreshes the scoreboard every 5 minutes.
- Includes Olympic rings for a thematic touch.

## Prerequisites

- Python 3.x
- Flask
- pandas

## Installation

1. **Clone the repository**:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install the required Python packages**:

    ```sh
    pip install flask pandas
    ```

3. **Ensure you have the CSV file (`scores.csv`) in the same directory as `scoreboard.py`**. The CSV file should have the following structure:

    ```csv
    Team Name,Event 1,Event 2,Event 3,Event 4,Event 5
    Team A,10,20,30,40,50
    Team B,15,25,35,45,55
    Team C,20,30,40,50,60
    ```

## Usage

1. **Run the Flask application**:

    ```sh
    python scoreboard.py
    ```

2. **Open your web browser and navigate to** `http://127.0.0.1:5000` **to view the scoreboard**.

The web page will display the scoreboard and automatically refresh every 5 minutes to update the scores.

## Code Explanation

### `scoreboard.py`

The script performs the following tasks:

1. **Read Scores**: Reads the scores from `scores.csv` and calculates the total scores for each team.
2. **Sort Teams**: Sorts the teams based on their total scores in descending order.
3. **Assign Classes**: Assigns CSS classes (`gold`, `silver`, `bronze`) to the top three teams.
4. **Render Template**: Uses Flask to render the scoreboard template with the teams and their scores.
5. **Auto-refresh**: The web page automatically refreshes every 5 minutes to update the scores.

### HTML Template

The HTML template used in the script includes:

- A header with the title and an icon.
- An SVG image of the Olympic rings.
- A table to display the team names, event scores, and total scores.
- CSS styles for a modern look and feel.

### Auto-refresh

The JavaScript `setTimeout` function is used to reload the page every 5 minutes:

```javascript
setTimeout(function() {
  window.location.reload(1);
}, 300000);
