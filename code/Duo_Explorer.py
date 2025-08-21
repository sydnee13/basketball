import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import percentileofscore

all_stats = pd.read_csv("data/all_stats.csv")
stats_2324 = pd.read_csv("data/stats_2324.csv")
st.set_page_config(layout="centered")

new_title = '<p style="font-family:sans-serif; color:Black; font-size: 42px;">Duo Compatibility Explorer</p>'
st.markdown(new_title, unsafe_allow_html=True)

new_title = '<p style="font-family:sans-serif; color:Green; font-size: 26px;">Find Your Duo</p>'
st.markdown(new_title, unsafe_allow_html=True)

unique_players = pd.concat([all_stats['Player_1'], all_stats['Player_2']]).sort_values().unique()
player_list = [None] + unique_players.tolist() 

def categorize_score(score):
    if score >= 95:
        return "Dynasty Duo 💍"
    elif score >= 90:
        return "All-Star Chemistry ⭐️"
    elif score >= 80:
        return "Elite Sync 🔥"
    elif score >= 70:
        return "Playoff Ready 🏆"
    elif score >= 60:
        return "Solid Pairing 💪"
    elif score >= 50:
        return "Team Players 🤝"
    elif score >= 40:
        return "Work in Progress 🛠️"
    elif score >= 30:
        return "Mismatch Madness 🤯"
    elif score >= 20:
        return "On-Court Strangers 😬"
    else:
        return "Oil & Water 🧪"

col1, col2 = st.columns([2, 2], gap="large")
with col1:
    p1 = st.selectbox("Select Player 1", player_list, index=0)  
with col2:
    p2 = st.selectbox("Select Player 2", player_list, index=0)

fig = px.histogram(all_stats, x='Score', nbins=100, title='Histogram of Compatibility Scores')
if p1 and p2:
    mask = ((all_stats['Player_1'] == p1) & (all_stats['Player_2'] == p2)) | \
           ((all_stats['Player_1'] == p2) & (all_stats['Player_2'] == p1))
    match = all_stats[mask]
    if not match.empty:
        score = match['Score'].values[0]
        category = categorize_score(score)
        fig.add_vline(x=score, line_width=3, line_dash="dash", line_color="red",
                      annotation_text=f"{p1} & {p2}: {score:.2f}", 
                      annotation_position="top left")
        percentile = percentileofscore(all_stats['Score'], score, kind='rank') 
        percent_better_than = round(percentile - 0.5, 1) 
        st.markdown(f"### Compatibility Score: `{score:.2f}`")
        st.markdown(f"### Category: **{category}**")
        st.markdown(f"### Better than **{percent_better_than}%** of all duos!")

st.plotly_chart(fig)

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

def plot_cluster():
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
    if p1 != "None":
        player_df = df[df["Player"] == p1]
        fig.add_trace(go.Scatter(
            x = player_df["PC1"],
            y = player_df["PC2"],
            mode = "markers",
            marker = dict(color="orange", size=16),
            showlegend = False,
            hoverinfo = "skip"
        ))
    if p2 != "None":
        player_df = df[df["Player"] == p2]
        fig.add_trace(go.Scatter(
            x = player_df["PC1"],
            y = player_df["PC2"],
            mode = "markers",
            marker = dict(color="green", size=16),
            showlegend = False,
            hoverinfo = "skip"
        ))
    fig.update_layout(
        xaxis_title = "PC1",
        yaxis_title = "PC2",
        width=800, 
        height=600,
        legend_title = "Clusters"
        )
    st.plotly_chart(fig)
plot_cluster()



