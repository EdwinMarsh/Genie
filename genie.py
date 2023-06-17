import pandas as pd
import tkinter as tk  # pylint: disable=import-error
from tkinter import ttk  # pylint: disable=import-error
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('results.csv')


def calculate_performance(matches):
    total_matches = len(matches)
    if total_matches == 0:
        return 0, 0, 0

    home_wins = len(matches[matches['home_score'] > matches['away_score']])
    away_wins = len(matches[matches['home_score'] < matches['away_score']])
    draws = len(matches[matches['home_score'] == matches['away_score']])
    losses = total_matches - home_wins - away_wins - draws

    home_win_percentage = (home_wins / total_matches) * 100
    away_win_percentage = (away_wins / total_matches) * 100
    draw_percentage = (draws / total_matches) * 100
    loss_percentage = (losses / total_matches) * 100

    return home_win_percentage, away_win_percentage, draw_percentage, loss_percentage


def get_last_matches(team, n=5):
    team_matches = df[(df['home_team'] == team) | (df['away_team'] == team)]
    last_matches = team_matches.tail(n)
    return last_matches[['date', 'home_team', 'away_team', 'home_score', 'away_score']]

def plot_performance_progress():
    home_team = home_team_entry.get()
    away_team = away_team_entry.get()

def plot_performance_progress():
    home_team = home_team_entry.get()
    away_team = away_team_entry.get()

    # Filter the data for the specified teams
    home_matches = df[(df['home_team'] == home_team) | (df['away_team'] == home_team)]
    away_matches = df[(df['home_team'] == away_team) | (df['away_team'] == away_team)]

    # Calculate current performance for home team
    total_home_matches = len(home_matches)
    home1_wins = len(home_matches[((home_matches['home_team'] == home_team) & (
                home_matches['home_score'] > home_matches['away_score'])) |
                                  ((home_matches['away_team'] == home_team) & (
                                              home_matches['away_score'] > home_matches['home_score']))])
    draws1 = len(home_matches[((home_matches['home_team'] == home_team) & (
                home_matches['home_score'] == home_matches['away_score'])) |
                              ((home_matches['away_team'] == home_team) & (
                                          home_matches['home_score'] == home_matches['away_score']))])
    home_losses1 = total_home_matches - home1_wins - draws1

    home1_win_percentage = (home1_wins / total_home_matches) * 100
    draw1_percentage = (draws1 / total_home_matches) * 100
    home1_loss_percentage = (home_losses1 / total_home_matches) * 100

    # Calculate current performance for away team
    total_away_matches = len(away_matches)
    away_wins = len(away_matches[((away_matches['home_team'] == away_team) & (
                away_matches['home_score'] < away_matches['away_score'])) |
                                 ((away_matches['away_team'] == away_team) & (
                                             away_matches['away_score'] > away_matches['home_score']))])
    draws2 = len(away_matches[((away_matches['home_team'] == away_team) & (
                away_matches['home_score'] == away_matches['away_score'])) |
                              ((away_matches['away_team'] == away_team) & (
                                          away_matches['home_score'] == away_matches['away_score']))])
    away_losses2 = total_away_matches - away_wins - draws2

    away_win_percentage = (away_wins / total_away_matches) * 100
    draw2_percentage = (draws2 / total_away_matches) * 100
    away_loss_percentage = (away_losses2 / total_away_matches) * 100

    # Display current performance
    current_performance_text = f"Current Performance:\n\n"
    current_performance_text += f"{home_team}:\nWin %: {home1_win_percentage:.2f}%\n"
    current_performance_text += f"Draw %: {draw1_percentage:.2f}%\n"
    current_performance_text += f"Loss %: {home1_loss_percentage:.2f}%\n\n"

    current_performance_text += f"{away_team}:\nWin %: {away_win_percentage:.2f}%\n"
    current_performance_text += f"Draw %: {draw2_percentage:.2f}%\n"
    current_performance_text += f"Loss %: {away_loss_percentage:.2f}%\n\n"

    current_performance_label.config(text=current_performance_text)

    # Calculate head-to-head performance
    head_to_head_matches = df[((df['home_team'] == home_team) & (df['away_team'] == away_team)) |
                              ((df['home_team'] == away_team) & (df['away_team'] == home_team))]
    if len(head_to_head_matches) > 0:
        head_to_head_home_win_percentage, head_to_head_away_win_percentage, head_to_head_draw_percentage, head_to_head_loss_percentage = calculate_performance(
            head_to_head_matches)
        head_to_head_performance_text = f"Head-to-Head Performance:\n\n"
        head_to_head_performance_text += f"{home_team}:\nWin %: {head_to_head_home_win_percentage:.2f}%\n"
        head_to_head_performance_text += f"{away_team}:\nWin %: {head_to_head_away_win_percentage:.2f}%\n"
        head_to_head_performance_label.config(text=head_to_head_performance_text)
    else:
        head_to_head_performance_label.config(text="No matches between these teams.")

    # Get the last matches of each team
    home_last_matches = get_last_matches(home_team)
    away_last_matches = get_last_matches(away_team)
    home_last_matches_label.config(text=f"Last Matches of {home_team}:")
    away_last_matches_label.config(text=f"Last Matches of {away_team}:")

    # Clear the existing table data
    home_table.delete(*home_table.get_children())
    away_table.delete(*away_table.get_children())

    for i, row in home_last_matches.iterrows():
        home_table.insert('', 'end', values=row.tolist())

    for i, row in away_last_matches.iterrows():
        away_table.insert('', 'end', values=row.tolist())

    # Prepare data for the plot
    home_team_scores = home_last_matches['home_score'].tolist() + away_last_matches['away_score'].tolist()
    away_team_scores = home_last_matches['away_score'].tolist() + away_last_matches['home_score'].tolist()
    match_dates = home_last_matches['date'].tolist() + away_last_matches['date'].tolist()

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(match_dates, home_team_scores, color='b', marker='o', label=home_team)
    plt.plot(match_dates, away_team_scores, color='r', marker='o', label=away_team)

    plt.xlabel('Date')
    plt.ylabel('Number of Goals')
    plt.title(f'Last 10 Matches: {home_team} vs {away_team}')
    plt.legend()
    plt.show()


# Create the GUI window
window = tk.Tk()
window.title("Football Match Predictor")

# Create the labels, entries, and button
home_team_label = tk.Label(window, text="Home Team:")
home_team_label.pack()
home_team_entry = tk.Entry(window)
home_team_entry.pack()

away_team_label = tk.Label(window, text="Away Team:")
away_team_label.pack()
away_team_entry = tk.Entry(window)
away_team_entry.pack()

predict_button = tk.Button(window, text="Predict", command=plot_performance_progress)
predict_button.pack()

# Create the left canvas to display current performance
left_canvas = tk.Canvas(window, width=300, height=200, bg='white')
left_canvas.pack(side=tk.LEFT)

current_performance_label = tk.Label(left_canvas, text="", anchor='w')
current_performance_label.pack()

# Create the right canvas to display head-to-head performance
right_canvas = tk.Canvas(window, width=300, height=200, bg='white')
right_canvas.pack(side=tk.RIGHT)

head_to_head_performance_label = tk.Label(right_canvas, text="", anchor='w')
head_to_head_performance_label.pack()

# Create the frame to display the last matches
last_matches_frame = tk.Frame(window)
last_matches_frame.pack()

# Create the labels to display the last matches
home_last_matches_label = tk.Label(last_matches_frame, text="Last Matches of Home Team:")
home_last_matches_label.pack(side=tk.TOP)

home_table = ttk.Treeview(last_matches_frame,
                          columns=('Date', 'Home Team', 'Away Team', 'Home Score', 'Away Score'), show='headings')

home_table.heading('Date', text='Date')
home_table.heading('Home Team', text='Home Team')
home_table.heading('Away Team', text='Away Team')
home_table.heading('Home Score', text='Home Score')
home_table.heading('Away Score', text='Away Score')
home_table.pack(side=tk.TOP)

away_last_matches_label = tk.Label(last_matches_frame, text="Last Matches of Away Team:")
away_last_matches_label.pack(side=tk.TOP)

away_table = ttk.Treeview(last_matches_frame,
                          columns=('Date', 'Home Team', 'Away Team', 'Home Score', 'Away Score'), show='headings')

away_table.heading('Date', text='Date')
away_table.heading('Home Team', text='Home Team')
away_table.heading('Away Team', text='Away Team')
away_table.heading('Home Score', text='Home Score')
away_table.heading('Away Score', text='Away Score')
away_table.pack(side=tk.BOTTOM)

# Create the canvas to display the plot
plot_canvas = tk.Canvas(window, width=800, height=400)
plot_canvas.pack()

# Start the GUI event loop
window.mainloop()
