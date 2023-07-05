


"""
Ceara Zhang
DS 3500 / SunDash
Sunspot Dashboard / Homework 2
Created 2/1/2023

"""
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


# read csv
sun = pd.read_csv('SN_m_tot_V2.0.csv')

# adding a column name
sun.columns = ['string']

# split the single column by the semicolon to create 7 columns
sun['new string'] = sun['string'].str.split(';')

# create the 7 columns and fill NA with empty strings
sun = pd.DataFrame(sun['new string'].tolist()).add_prefix('mod')

# rename the columns with descriptive headers
sun = sun.rename(columns={'mod0': 'year', 'mod1': 'month', 'mod2': 'yr_fraction',
                          'mod3': 'monthly_mean', 'mod4': 'monthly_std',
                          'mod5': 'num_obs', 'mod6': 'definitive?'})

# apply string type to everything to clean up excess spaces,
# then casting types as int or float
sun = sun.applymap(str)
sun['year'] = sun['year'].str.replace(" ", "").astype(int)
sun['month'] = sun['month'].str.replace(" ", "").astype(int)
sun['yr_fraction'] = sun['yr_fraction'].str.replace(" ", "").astype(float)
sun['monthly_mean'] = sun['monthly_mean'].str.replace(" ", "").astype(float)
sun['monthly_std'] = sun['monthly_std'].str.replace(" ", "").astype(float)
sun['num_obs'] = sun['num_obs'].str.replace(" ", "").astype(int)
sun['definitive?'] = sun['definitive?'].str.replace(" ", "").astype(int)

# using only relevant columns
sun = sun[['year', 'month', 'yr_fraction', 'monthly_mean']]

# remove invalid data represented by -1
sun = sun[~(sun == -1).any(axis=1)]

# add a new column for the rolling averages
sun['rolling_mean_vals'] = sun['monthly_mean']

# display years on the range slider as strings
marks = {1749: {'label': '1749'},
         1774: {'label': '1774'},
         1799: {'label': '1799'},
         1824: {'label': '1824'},
         1849: {'label': '1849'},
         1874: {'label': '1874'},
         1899: {'label': '1899'},
         1924: {'label': '1924'},
         1949: {'label': '1949'},
         1974: {'label': '1974'},
         1999: {'label': '1999'},
         2024: {'label': '2024'}}

monthly_marks = {1: {'label': 'Jan'},
                 2: {'label': 'Feb'},
                 3: {'label': 'Mar'},
                 4: {'label': 'Apr'},
                 5: {'label': 'May'},
                 6: {'label': 'Jun'},
                 7: {'label': 'Jul'},
                 8: {'label': 'Aug'},
                 9: {'label': 'Sept'},
                 10: {'label': 'Oct'},
                 11: {'label': 'Nov'},
                 12: {'label': 'Dec'}}

# defining the app
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H2('SOLAR INFORMATION DASHBOARD'
                )
    ],
        className="app__header"
    ),

    # dropdown of different sun images
    html.Div([
        dcc.Dropdown(
            id='image_dropdown',
            options=[
                {'label': 'Real Time Sun Image', 'value': 'https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg'},
                {'label': 'EIT 171', 'value': 'https://soho.nascom.nasa.gov/data/realtime/eit_171/1024/latest.jpg'},
                {'label': 'EIT 195', 'value': 'https://soho.nascom.nasa.gov/data/realtime/eit_195/1024/latest.jpg'},
                {'label': 'EIT 284', 'value': 'https://soho.nascom.nasa.gov/data/realtime/eit_284/1024/latest.jpg'},
                {'label': 'EIT 304', 'value': 'https://soho.nascom.nasa.gov/data/realtime/eit_304/1024/latest.jpg'},
                {'label': 'SDO/HMI Continuum', 'value': 'https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg'},
                {'label': 'SDO/HMI Magnetogram', 'value': 'https://soho.nascom.nasa.gov/data/realtime/hmi_mag/1024/latest.jpg'},
                {'label': 'SOHO LASCO C2', 'value': 'https://soho.nascom.nasa.gov/data/realtime/c2/1024/latest.jpg'},
                {'label': 'SOHO LASCO C3', 'value': 'https://soho.nascom.nasa.gov/data/realtime/c3/1024/latest.jpg'}
            ],
            value='https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg'
        ),
        html.Img(id='image', style={'width': '550px', 'height': '550px'})
    ],
        style={'display': 'inline-block'}
    ),

    # plot 2: show sunspot variability over a cycle (years)
    html.Div([

        # title and graph
        html.Div([
            dcc.Graph(id='sunspot_count_plot')
        ]
        ),

        # controls the cycle length displayed
        html.Div([
            html.P("Cycle length (years):  "),
            dcc.Input(id='cycle_length',
                      type='number',
                      value=11.0,
                      style={'display': 'flex', 'justifyContent': 'center'}),
        ],
            style={'top': '-100'}
        ),

        # controls the range of months displayed
        html.Div([
            html.P("Range of months to display"),
            dcc.RangeSlider(id='month_range',
                            min=1,
                            max=12,
                            value=[1, 12],
                            marks=monthly_marks)
        ]
        )
    ],
        style={'display': 'inline-block', 'float': 'right'}
    ),

    # plot1: sunspot number graph
    html.Div([

        # title and graph
        html.Div([
            html.H3("Mean Sunspot Activity Over a Range of Years"),
            dcc.Graph(id="sunspot_graph")
        ]
        ),

        # slider to select years to display in
        # x-axis of sunspot graph
        html.Div([
            html.P("Select the range of years to be displayed:"),
            dcc.RangeSlider(id='year_range',
                            min=1749,
                            max=2025,
                            value=[1949, 2022],
                            marks=marks),
        ]
        ),

        # slider to select the window size to
        # adjust the smoothing of line in sunspot graph
        html.Div([
            html.P("Select the smoothing value to adjust the smoothing average line:"),
            dcc.Slider(id='window_size',
                       min=1,
                       max=15,
                       step=1,
                       value=8),

        ]
        )
    ],
        style={'margin-top': '800'}
    ),

]
)


@app.callback(
    Output('image', 'src'),
    [Input('image_dropdown', 'value')])
def update_image(value):

    return value


# Plot 1: Mean Sunspot Activity Over a Range of Years
@app.callback(
    # output: graph with monthly mean sunspot numbers
    # input: display what range of years, and the smoothing value
    Output("sunspot_graph", "figure"),
    [Input("year_range", "value"),
     Input("window_size", "value")])
def update_plot1(year_range, window_size):
    """
    Write 1 short sentence about what this function will be doing
    :param year_range: (list) a min and max for years
    :param window_size: (int) smoothing line value
    :return: produces a line plots with 2 lines: the main data plot
    smoothing average
    """

    # filter column x to only contain the specified date range
    filter_range_sun = sun[(sun['yr_fraction'] >= year_range[0]) & (sun['yr_fraction'] <= year_range[1])].copy()

    # calculate rolling mean with given window size on the filtered df
    filter_range_sun['rolling_mean_vals'] = filter_range_sun['monthly_mean'].rolling(window=window_size).mean()

    # plot the data and the smoothing line
    fig = px.line(filter_range_sun,
                  x="yr_fraction",
                  y="monthly_mean",
                  labels={"yr_fraction": "Year",
                          "monthly_mean": "Mean Number of Sunspots"})
    fig.add_scatter(name="smoothing average",
                    x=filter_range_sun['yr_fraction'],
                    y=filter_range_sun['rolling_mean_vals'])

    return fig


# Plot 2: Sunspot Variability Over a Period of User Defined Years
@app.callback(
    # output: sunspot variability plot
    # input: cycle length (yrs)
    Output('sunspot_count_plot', 'figure'),
    [Input('cycle_length', 'value'),
     Input('month_range', 'value')])
def update_plot2(cycle_length, month_range):
    """
    This function updates the sunspot variability plot visual
    :param cycle_length: (int) cycle length in years
    :param month_range: (list) a min and max for months
    :return: produces a scatter plot
    """
    # calculate modulus of cycle length
    sun['modulus'] = sun['yr_fraction'] % cycle_length

    # filter the dataframe to only return rows in the given range of months
    filter_range_months_sun = sun[(sun['month'] >= month_range[0]) & (sun['month'] <= month_range[1])].copy()

    # plot the scatter plot, given the period for years as the x-axis
    fig = px.scatter(x=filter_range_months_sun['modulus'],
                     y=filter_range_months_sun['monthly_mean'],
                     labels={'x': "Years",
                             'y': "Mean Number of Sunspots"},
                     title="Sunspot Variability Over a Period of:  " + str(cycle_length) + " Years",
                     width=800,
                     height=450)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
