# Import pacakage for the exercice
import mysql.connector
import pandas as pd
import streamlit as st
import seaborn as sns
from matplotlib import pyplot as plt

# Set a title to the page
st.title('WCS Challenge : Cars analyse')

# Set links to navigate in the page
# links = ["<a href='#Logistic'>Logistic</a>",\
#          "<a href='#Finances'>Finances </a>",\
#          #"<a href='#finances-2'>Finances 2</a>",\
#          "<a href='#Sales'>Sales</a>",\
#          "<a href='#Human-Resources'>Human Resources</a>"]
# for l in links:
#     st.sidebar.write(
#         l,
#         unsafe_allow_html=True
#     )

# Get the CSV link
link = "https://raw.githubusercontent.com/FMrtnz/video_game_project/main/vgsales.csv"
# READ the CSV link with pandas then display
df_games = pd.read_csv(link)

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

# Set correlation then see the chart with
fig, ax = plt.subplots()
viz_correlation = sns.heatmap(
                            df_games.corr(),
							center=0,
							cmap = sns.color_palette("vlag", as_cmap=True)
							)
# We replace plt.show() by st.pyplot()
st.pyplot(viz_correlation.figure, clear_figure=True)

# Set list of colors for each country
#colors = {regions_list[0]: "red" , regions_list[1]:"orange", regions_list[2]:"green"}

# define a function to create differents plots scatter
def loop_plot_scatter(x_axis, y_axis_cols):
    for col in y_axis_cols:
        fig, ax = plt.subplots()
        for region in labels_countries:
            # Select the region for each axe
            # Use plot function from panda to set | kind is a param to set plot type
            df_games[df_games['continent'] == region].copy().plot(kind="scatter",\
            # ax allows us to association to a fig position\
            ax = ax, \
            # Setting X and Y axis\
            x=x_axis, y=col, ylabel=col, figsize= (10, 3), \
            # Define color for axe with the color list created \
            color = colors[region])
        ax.legend(labels_countries)
        st.pyplot(fig)

def loop_plot_box(x_axis, y_axis_cols):
    fig = plt.figure(figsize=(10, 15))
    i = 1
    for col in y_axis_cols:
        ax = plt.subplot(2,2,i)
        df_games.boxplot(by=x_axis, column=col, ax=ax)
        ax.set( title = f"{col} vs {x_axis}" )
        i += 1
    st.pyplot(fig)
