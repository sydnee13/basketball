import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

all_stats = pd.read_csv("data/all_stats.csv")
stats_2324 = pd.read_csv("data/stats_2324.csv")
st.set_page_config(layout="centered")

new_title = '<p style="font-family:sans-serif; color:Black; font-size: 42px;">Kevin Durant Trade Evaluator</p>'
st.markdown(new_title, unsafe_allow_html=True)

unique_players = pd.concat([all_stats['Player_1'], all_stats['Player_2']]).sort_values().unique()
player_list = ["None"] + unique_players.tolist() 
player1 = st.selectbox("Select a player to trade", player_list, index=0)
teams = ["None", 'ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 
        'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
trade_team = st.selectbox("Select a team to trade to", teams, index=0)  

# Only run trade logic if both selections are valid
if player1 != "None" and trade_team != "None":
    re = all_stats[(all_stats["Player_1"] == player1) | (all_stats["Player_2"] == player1)]
    
    if player1 in all_stats["Player_1"].values:
        team = all_stats.loc[all_stats["Player_1"] == player1, "Team 1"].iloc[0]
    elif player1 in all_stats["Player_2"].values:
        team = all_stats.loc[all_stats["Player_2"] == player1, "Team 2"].iloc[0]
    else:
        team = None  # In case somehow not found
    
    re1 = re[re["Team 1"] != team]
    re2 = re[re["Team 2"] != team]

    if trade_team == team:
        st.markdown("### No Can Do :(")
    elif trade_team in re2["Team 2"].values:
        scores = re2[re2["Team 2"] == trade_team][["Player_1", "Player_2", "Score"]]
        st.dataframe(scores.reset_index(drop=True), use_container_width=True)
        st.markdown(f"Average Score = {scores['Score'].mean():.2f}")
    elif trade_team in re1["Team 1"].values:
        scores = re1[re1["Team 1"] == trade_team][["Player_1", "Player_2", "Score"]]
        st.dataframe(scores.reset_index(drop=True), use_container_width=True)
        st.markdown(f"Average Score = {scores['Score'].mean():.2f}")
    else:
        st.markdown("### No data found for this trade team 🤷‍♀️")

player = st.selectbox("Select a player to compare", player_list, index=0)
if player != "None" and player1 != "None":
    if player == player1:
        st.markdown("### No Can Do :(")
    else:
        scores2 = re[
            ((re["Player_1"] == player) & (re["Player_2"] == player1)) |
            ((re["Player_2"] == player) & (re["Player_1"] == player1))
        ]
        st.dataframe(scores2[["Player_1", "Player_2", "Score"]].reset_index(drop=True), use_container_width=True)

    
    