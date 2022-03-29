# Import pacakage for the exercice
import mysql.connector
import pandas as pd
import streamlit as st
import seaborn as sns
from matplotlib import pyplot as plt

# Set a title to the page
st.title('WCS Challenge : Video Game analyse')

# Get the CSV link
link = "https://raw.githubusercontent.com/FMrtnz/video_game_project/main/vgsales.csv"
# READ the CSV link with pandas then display
df_games = pd.read_csv(link)

# Get title len
df_games["Title's length"] = df_games["Name"].apply(len)
df_games["Count words"] = df_games["Name"].apply(lambda name: len(name.split(" ")) )
#df_games["average letters by words"] = df_games[["Title's length", "Count words"]].apply(lambda row: row[0] / row[1] )
st.subheader("Table Video games")
df_games

# st.write is like a print function of python tyo display results
st.subheader("NaN elements")
if(df_games.isnull().sum().sum() > 0):
    st.warning('There are NaN in the table')
    st.write(df_games.isnull().sum())
    st.write('Total rows', len(df_games.index) )
    st.write('Total columns', len(df_games.columns) )
else:
    st.write("No NaN found in the table")
    st.write('Total rows', len(df_games.index) )
    st.write('Total columns', len(df_games.columns) )

st.subheader("Statistics' observations")
# st.write is like a print function of python tyo display results
st.write(df_games.describe())

st.subheader("Correlation")

#st.write(df_games.corr())

# Set correlation then see the chart with
fig, ax = plt.subplots()
viz_correlation = sns.heatmap(
                            df_games.corr(),
							center=0,
							cmap = sns.color_palette("vlag", as_cmap=True)
							)
# We replace plt.show() by st.pyplot()
st.pyplot(viz_correlation.figure, clear_figure=True)

top_5_publisher = df_games.groupby(["Publisher"])["Global_Sales", "NA_Sales","EU_Sales","JP_Sales","Other_Sales"].sum().sort_values(["Global_Sales"], ascending=False)
st.write(top_5_publisher.head())

st.write(df_games.groupby(["Publisher"])['Platform', "Genre"].count().sort_values(['Platform', "Genre"]))
