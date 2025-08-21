import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.graph_objects as go

stats_2324 = pd.read_csv("data/stats_2324.csv")
st.set_page_config(layout="centered")

columns = ['FGM', 'FGA','FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 
           'OREB','ORB_PCT', 'DREB', 'DRB_PCT', 'AST', 'AST_PCT', 'STL', 'STL_PCT', 
           'BLK','BLK_PCT', 'TOV', 'TOV_PCT', 'PF', 'PTS']
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

new_title = '<p style="font-family:sans-serif; color:Black; font-size: 42px;">PCA Playing Style Clustering</p>'
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
        title = "NBA Players Clusters",
        xaxis_title = "PC1",
        yaxis_title = "PC2",
        width=800, 
        height=600,
        legend_title = "Clusters"
        )
    st.plotly_chart(fig)

    if team_name != "None":
        st.dataframe(team_df[["Player Name", "Team", "Cluster", "PC1", "PC2"]])

plot_cluster(team_name)

