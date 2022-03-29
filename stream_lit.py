# Import pacakage for the exercice
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set a title to the page
st.title('WCS Challenge : Cars analyse')

# Set links to navigate in the page
links = '<ul><li><a href="#table-cars">Table cars</a></li>'
links += '<li><a href="#nan-elements">NaN elements</a></li>'
links += '<li><a href="#statistics-observations">Statistics observations</a></li>'
links += '<li><a href="#correlation">Correlation</a></li></ul>'
st.markdown(links, unsafe_allow_html=True)

# Get the CSV link
link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
# READ the CSV link with pandas then display
df_cars = pd.read_csv(link)

# Set the available country
regions_list = df_cars.groupby(["continent"]).count().index.values

# Set an input to choose region
regions_selected = st.multiselect(
 'Filter by region(s) available in Dataframe',
 regions_list
)

st.subheader("Table cars")
if len(regions_selected) > 0:
    # Adaptative variable for plots
    labels_countries = regions_selected
    # Adaptative DataFrame
    df_filtered = df_cars[df_cars['continent'].isin(regions_selected)]
else:
    df_filtered = df_cars
    labels_countries = regions_list

df_filtered

st.subheader("Columns description")
st.markdown('MPG (Mille per Gallon): Describe how many milles a car cans do per gallon')
st.markdown('Cylinders (number in the car): The number of the cylinders defines the power of the car.')
st.markdown("Cubicinches: Unity of Motor's volume")
st.markdown("Hp (Horse power): Unity of Motor's power ")
st.markdown("Weightlbs: Car's weight in Pound")
st.markdown('time-to-60: Time to arrive at 60 milles per hour')

# st.write is like a print function of python tyo display results
st.subheader("NaN elements")
if(df_filtered.isnull().sum().sum() > 0):
    st.warning('There are NaN in the table')
    st.write(df_filtered.isnull().sum())
    st.write('Total rows', len(df_filtered.index) )
    st.write('Total columns', len(df_filtered.columns) )
else:
    st.write("No NaN found in the table")
    st.write('Total rows', len(df_filtered.index) )
    st.write('Total columns', len(df_filtered.columns) )

st.subheader("Statistics' observations")
# st.write is like a print function of python tyo display results
st.write(df_filtered.describe())

st.subheader("Correlation")

# Set correlation then see the chart with
fig, ax = plt.subplots()
viz_correlation = sns.heatmap(
                            df_filtered.corr(),
							center=0,
							cmap = sns.color_palette("vlag", as_cmap=True)
							)
# We replace plt.show() by st.pyplot()
st.pyplot(viz_correlation.figure, clear_figure=True)

# Set list of colors for each country
colors = {regions_list[0]: "red" , regions_list[1]:"orange", regions_list[2]:"green"}

# define a function to create differents plots scatter
def loop_plot_scatter(x_axis, y_axis_cols):
    for col in y_axis_cols:
        fig, ax = plt.subplots()
        for region in labels_countries:
            # Select the region for each axe
            # Use plot function from panda to set | kind is a param to set plot type
            df_filtered[df_filtered['continent'] == region].copy().plot(kind="scatter",\
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
        df_filtered.boxplot(by=x_axis, column=col, ax=ax)
        ax.set( title = f"{col} vs {x_axis}" )
        i += 1
    st.pyplot(fig)

#Loop to create plot with mpg as x-axis
#Define list of plot to create
cols = ["cubicinches","hp","weightlbs","time-to-60"]
x_axis="mpg"
loop_plot_scatter(x_axis, cols)

#Loop to create plot with x-axis cylinders
cols_2 = ["mpg", "cubicinches", "hp","weightlbs","time-to-60"]
x_axis="cylinders"
#loop_plot_scatter(x_axis, cols_2)

# test = pd.pivot_table(df_cylinders, columns="continent")
# st.write()
#
for col in cols_2:
  fig, ax = plt.subplots()
  #for region in labels_countries:
  df_filtered.copy().groupby(['continent', x_axis])[col].count().unstack(level=0).plot(kind="bar",ax = ax, rot=0, figsize= (10, 3))
  #ax.legend(labels_countries)
  st.pyplot(fig)


#Loop to create plot with x-axis cubicinches
cols_3 = ["cubicinches", "hp","weightlbs","time-to-60"]
x_axis = "continent"
loop_plot_box(x_axis, cols_3)

#Loop to create plot with x-axis hp
cols_4 = ["weightlbs","time-to-60"]
x_axis = "hp"
loop_plot_scatter(x_axis, cols_4)

#Loop to create plot with x-axis year
cols_5 = ["mpg","time-to-60"]
x_axis = "year"
df_means = df_filtered.copy().groupby(['continent', x_axis], as_index=False).mean()

for col in cols_5:
  fig, ax = plt.subplots()
  for region in labels_countries:
      df_means[df_means['continent'] == region].plot(kind="line",ax = ax, x=x_axis, y=col, ylabel=col, figsize= (10, 3), color = colors[region])
  ax.legend(labels_countries)
  st.pyplot(fig)
