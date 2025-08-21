import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
import plotly.express as px
import plotly.graph_objects as go

alllineup_stats = pd.read_csv("alllineup_stats.csv")
stats_2324 = pd.read_csv("stats_2324.csv")
hypothetical_duos = pd.read_csv("hypothetical_duos.csv")
st.set_page_config(layout="centered")
st.write("""
# NBA Basketball Compatibility
SARGS Checkpoint 2 - Sydnee Chang
""")

st.markdown("<h3>There are 36,832 possible 2-man player lineups. Below is a distribution of their compatibility scores.</h3>", unsafe_allow_html=True)

mean_score = hypothetical_duos["Score"].mean()
# median_score = hypothetical_duos["Score"].median()
std_score = hypothetical_duos["Score"].std()
fig = px.histogram(hypothetical_duos, x="Score", nbins=100, 
                   title="Distribution of Scores", 
                   labels={"Score": "Score"},
                   opacity=0.7)
fig.add_vline(x=mean_score, line=dict(color="blue", dash="dash"), 
              annotation_text=f"Mean: {mean_score:.2f}", annotation_position="top left")
st.plotly_chart(fig, use_container_width=True)



new_title = '<p style="font-family:sans-serif; color:Green; font-size: 26px;">Find Your Duo</p>'
st.markdown(new_title, unsafe_allow_html=True)

unique_players = pd.concat([hypothetical_duos['Player_1'], hypothetical_duos['Player_2']]).sort_values().unique()
player_list = unique_players.tolist()  

col1, col2 = st.columns([2, 2], gap="large")
with col1:
    p1 = st.selectbox("Select Player 1", player_list)
with col2:
    p2 = st.selectbox("Select Player 2", player_list)

def display_score(p1, p2):
    row = hypothetical_duos[
        ((hypothetical_duos['Player_1'] == p1) & (hypothetical_duos['Player_2'] == p2)) |
        ((hypothetical_duos['Player_1'] == p2) & (hypothetical_duos['Player_2'] == p1))
    ]
    if not row.empty:
        return row['Score'].iloc[0]  
    else:
        return None 

score = display_score(p1, p2)
if score is not None:
    compatibility = f"{score:.3f}% COMPATIBLE!"
else:
    compatibility = f"No compatibility data found for {p1} and {p2}."

p1_stats = stats_2324[stats_2324["Player"] == p1][["MIN", "PTS", "FGM", "FGA", "FG_PCT",
                                                   "FG3M", "FG3A", "FG3_PCT", "FT_PCT", "OREB", "DREB",
                                                   "AST", "STL", "BLK", "TOV", "PF"]]
p2_stats = stats_2324[stats_2324["Player"] == p2][["MIN", "PTS", "FGM", "FGA", "FG_PCT",
                                                   "FG3M", "FG3A", "FG3_PCT", "FT_PCT", "OREB", "DREB",
                                                   "AST", "STL", "BLK", "TOV", "PF"]]

p1_stats = p1_stats.T.reset_index()
p2_stats = p2_stats.T.reset_index()
p1_stats.columns = ["Stat", "Value"]
p2_stats.columns = ["Stat", "Value"]
p1_stats["Value"] = pd.to_numeric(p1_stats["Value"], errors="coerce").round(2)
p2_stats["Value"] = pd.to_numeric(p2_stats["Value"], errors="coerce").round(2)

st.header(compatibility)
col1, col2 = st.columns(2)  

with col1:
    st.write("Per 100 stats")
    st.dataframe(p1_stats, hide_index=True)
with col2:
    st.write("Per 100 stats")
    st.dataframe(p2_stats, hide_index=True)


columns = ['FGM', 'FGA','FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 
           'OREB','ORB_PCT', 'DREB', 'DRB_PCT', 'AST', 'AST_PCT', 'STL', 'STL_PCT', 
           'BLK','BLK_PCT', 'TOV', 'TOV_PCT', 'PF', 'PTS']
# columns = ['FG_PCT', 'FG3_PCT', 'FT_PCT', 'ORB_PCT', 'DRB_PCT', 'AST_PCT', 'STL_PCT', 'BLK_PCT', 'TOV_PCT']
stats_2324_mean = stats_2324[columns].mean()
stats_2324_std = stats_2324[columns].std()
standardized = (stats_2324[columns] - stats_2324_mean) / stats_2324_std
stats_2324_norm = stats_2324.copy()
stats_2324_norm[columns] = standardized

best_k = 6
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
stats_2324_norm['Cluster'] = kmeans.fit_predict(standardized)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(standardized)

stats_2324_norm['PC1'], stats_2324_norm['PC2'] = X_pca[:, 0], X_pca[:, 1]

new_title = '<p style="font-family:sans-serif; color:Green; font-size: 26px;">NBA Player Clustering</p>'
st.markdown(new_title, unsafe_allow_html=True)

teams = ["None", 'ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 
        'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
players = ["None"] + list(stats_2324_norm["Player"].sort_values().unique())
team_name = st.selectbox("Select a Team", teams)
player_name = st.selectbox("Select a Player", players)
player2_name = st.selectbox("Select Another Player", players)

def plot_cluster(team_name):
    df = stats_2324_norm.copy()
    df["Cluster"] = df["Cluster"].astype(str)
    cluster_order = sorted(df["Cluster"].unique(), key=int)
    fig = go.Figure()
    for cluster in cluster_order:
        cluster_df = df[df["Cluster"] == cluster]
        fig.add_trace(go.Scatter(
            x = cluster_df["PC1"],
            y = cluster_df["PC2"],
            mode = "markers",
            name = f"Cluster {cluster}",
            marker = dict(size=6),
            hovertext = cluster_df["Player"] + " (" + cluster_df["Team"] + ")"
        ))
    if team_name != "None":
        team_df = df[df["Team"] == team_name]
        fig.add_trace(go.Scatter(
            x = team_df["PC1"],
            y = team_df["PC2"],
            mode = "markers",
            marker = dict(color="purple", size=16),
            showlegend = False,
            hoverinfo = "skip"
        ))
    if player_name != "None":
        player_df = df[df["Player"] == player_name]
        fig.add_trace(go.Scatter(
            x = player_df["PC1"],
            y = player_df["PC2"],
            mode = "markers",
            marker = dict(color="orange", size=16),
            showlegend = False,
            hoverinfo = "skip"
        ))

    if player2_name != "None":
        player_df = df[df["Player"] == player2_name]
        fig.add_trace(go.Scatter(
            x = player_df["PC1"],
            y = player_df["PC2"],
            mode = "markers",
            marker = dict(color="green", size=16),
            showlegend = False,
            hoverinfo = "skip"
        ))
    fig.update_layout(
        title = "NBA Players Clustered (K-Means, PCA)",
        xaxis_title = "PC1",
        yaxis_title = "PC2",
        width=800, 
        height=600,
        legend_title = "Clusters"
        )
    st.plotly_chart(fig)

plot_cluster(team_name)


new_duos = hypothetical_duos[hypothetical_duos["Team 1"] != hypothetical_duos["Team 2"]].copy()
new_title = '<p style="font-family:sans-serif; color:Green; font-size: 26px;">Most Compatible Duos</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.dataframe(new_duos.head(10)[["Player_1", "Player_2", "Score"]])


new_title = '<p style="font-family:sans-serif; color:Green; font-size: 26px;">Least Compatible Duos</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.dataframe(new_duos.tail(10)[["Player_1", "Player_2", "Score"]])

# new_title = '<p style="font-family:sans-serif; color:Green; font-size: 26px;">Choose 2 players to look at their stats</p>'
# st.markdown(new_title, unsafe_allow_html=True)


# def spider(p1, p2):
#     players = alllineup_stats[((alllineup_stats["Player 1"] == p1) & (alllineup_stats["Player 2"] == p2)) | 
#                               ((alllineup_stats["Player 1"] == p2) & (alllineup_stats["Player 2"] == p1))]
#     selected = [6, 7, 8, 9, 10, 11, 13, 14, 16, 18, 22, 23, 24, 25, 26, 27, 28, 37, 38]
#     players_selected = players.iloc[0, selected]
#     players_df = pd.DataFrame(dict(
#         stat=players.columns[selected].tolist(),
#         value=players_selected.tolist()
#     ))

#     fig = px.line_polar(players_df, r='value', theta='stat', line_close=True)
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 range=[0, 100], 
#                 showticklabels=False
#             )
#         ),
#         title=f"{p1} and {p2}",
#         width=350,
#         height=350 
#     )
    
#     st.plotly_chart(fig, use_container_width=True)

# col1, col2 = st.columns([0.5,0.5], gap="small")

# with col1:
#     team_left = st.selectbox("Select Team (Left)", alllineup_stats["Team"].unique(), key="team_left")
#     players_in_team_left = alllineup_stats[alllineup_stats["Team"] == team_left]
#     unique_players_left = pd.concat([players_in_team_left["Player 1"], players_in_team_left["Player 2"]]).unique()
#     player1_left = st.selectbox("Select Player 1 (Left)", unique_players_left, key="player1_left")
#     player2_candidates_left = pd.concat([
#         players_in_team_left[players_in_team_left["Player 1"] == player1_left]["Player 2"],
#         players_in_team_left[players_in_team_left["Player 2"] == player1_left]["Player 1"]
#     ]).unique()
#     player2_left = st.selectbox("Select Player 2 (Left)", [player for player in player2_candidates_left if player != player1_left], key="player2_left")
    
#     if player1_left and player2_left:
#         spider(player1_left, player2_left)

# with col2:
    # team_right = st.selectbox("Select Team (Right)", alllineup_stats["Team"].unique(), key="team_right")
    # players_in_team_right = alllineup_stats[alllineup_stats["Team"] == team_right]
    # unique_players_right = pd.concat([players_in_team_right["Player 1"], players_in_team_right["Player 2"]]).unique()
    # player1_right = st.selectbox("Select Player 1 (Right)", unique_players_right, key="player1_right")
    # player2_candidates_right = pd.concat([
    #     players_in_team_right[players_in_team_right["Player 1"] == player1_right]["Player 2"],
    #     players_in_team_right[players_in_team_right["Player 2"] == player1_right]["Player 1"]
    # ]).unique()
    # player2_right = st.selectbox("Select Player 2 (Right)", [player for player in player2_candidates_right if player != player1_right], key="player2_right")

    # if player1_left == player1_right and player2_left == player2_right:
    #     st.warning("The same players have been selected in both columns. Please choose different players for each comparison.")
    # elif player1_right and player2_right:
    #     spider(player1_right, player2_right)

