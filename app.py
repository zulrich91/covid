import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
#import dash_auth
import json
import plotly.graph_objs as go
from io import BytesIO
import numpy as np
from scipy.integrate import odeint


agg_day_df = pd.read_csv('./data/agg_data_per_days.csv')
agg_reg = pd.read_csv('./data/agg_data_per_regions.csv',encoding='utf-8')
geo_labels = ["Nombre cumulé de personnes décédées pour COVID-19 depuis le 1er mars 2020 - hommes et femmes",
              "Nombre de personnes actuellement hospitalisées pour COVID-19 - hommes et femmes",
              "Nombre quotidien de nouveaux retours à domicile pour COVID-19",
              "Nombre quotidien de personnes nouvellement décédées pour COVID-19",
              "Nombre quotidien de nouvelles admissions en réanimation pour COVID-19",
              "Nombre quotidien de personnes nouvellement hospitalisées pour COVID-19",
              "Nombre de personnes actuellement en réanimation ou soins intensifs pour COVID-19 - hommes et femmes",
              "Nombre cumulé de personnes retournées à domicile depuis le 1er mars 2020 - hommes et femmes"]

preval_labels = ["Prévalences de l'anxiété pendant l’épidémie de Covid-19 (%)",
                "Prévalences de la dépression pendant l’épidémie de Covid-19 (%)",
                "Prévalences des problèmes de sommeil pendant l’épidémie de Covid-19 (%)",
                "Nombre moyen de mesures d’hygiène adoptées systématiquement pendant l’épidémie de Covid-19 (sur 4 mesures recommandées par les pouvoirs publics)",
                "Prévalences de l'adoption systématique du port du masque en public pendant l’épidémie de Covid-19 (%)",
                "Prévalence de l'adoption systématique des 4 mesures d’hygiène recommandées par les pouvoirs publics pendant l'épidémie de COVID-19 (%)"]
sir_labels = ['Overal SIR', "SIR per department"]
preval_drop_labels = ["13. 20-22 juillet",
                    "12. 6-8 juillet",
                    "11. 22-24 juin",
                    "10. 8-10 juin",
                    "09. 27-29 mai",
                    "08. 18-20 mai",
                    "07. 13-15 mai",
                    "06. 04-06 mai",
                    "05. 28-30 avril",
                    "04. 20-22 avril",
                    "03. 14-16 avril",
                    "02. 30 mars-01 avr"]
anxiety_labels = ["13. 20-22 juillet",
                    "12. 6-8 juillet",
                    "11. 22-24 juin",
                    "10. 8-10 juin",
                    "09. 27-29 mai",
                    "08. 18-20 mai",
                    "07. 13-15 mai",
                    "06. 04-06 mai",
                    "05. 28-30 avril",
                    "04. 20-22 avril",
                    "03. 14-16 avril",
                    "02. 30 mars-01 avril",
                    "01. 23-25 mars"]
# Anxiety dataset
anxiety_2022juillet_df = pd.read_csv("./prevalence/anxiety/clean/20-22-juillet.csv", encoding="utf-8" )
anxiety_0608juillet_df = pd.read_csv("./prevalence/anxiety/clean/6-8-juillet.csv", encoding="utf-8")
anxiety_2224juin_df = pd.read_csv("./prevalence/anxiety/clean/20-24-juin.csv", encoding="utf-8")
anxiety_0810juin_df = pd.read_csv("./prevalence/anxiety/clean/8-10-juin.csv", encoding="utf-8")
anxiety_2729mai_df = pd.read_csv("./prevalence/anxiety/clean/27-29-mai.csv", encoding="utf-8")
anxiety_1820mai_df = pd.read_csv("./prevalence/anxiety/clean/18-20-mai.csv", encoding="utf-8")
anxiety_1315mai_df = pd.read_csv("./prevalence/anxiety/clean/13-15-mai.csv", encoding="utf-8")
anxiety_0406mai_df = pd.read_csv("./prevalence/anxiety/clean/4-6-mai.csv", encoding="utf-8")
anxiety_2830avril_df = pd.read_csv("./prevalence/anxiety/clean/28-30-avril.csv", encoding="utf-8")
anxiety_2022avril_df = pd.read_csv("./prevalence/anxiety/clean/20-22-avril.csv", encoding="utf-8")
anxiety_1416avril_df = pd.read_csv("./prevalence/anxiety/clean/14-16-avril.csv", encoding="utf-8")
anxiety_30mars_01avr_df = pd.read_csv("./prevalence/anxiety/clean/30-mars-01-avril.csv", encoding="utf-8")
anxiety_df = [anxiety_2022juillet_df, anxiety_0608juillet_df, anxiety_2224juin_df, anxiety_0810juin_df, anxiety_2729mai_df,anxiety_1820mai_df,
            anxiety_1315mai_df,anxiety_0406mai_df, anxiety_2830avril_df, anxiety_2022avril_df ,anxiety_1416avril_df,anxiety_30mars_01avr_df ]

# depression datasets
depression_2022juillet_df = pd.read_csv("./prevalence/depression/clean/20-22-juillet.csv", encoding="utf-8")
depression_0608juillet_df = pd.read_csv("./prevalence/depression/clean/6-8-juillet.csv", encoding="utf-8")
depression_2224juin_df = pd.read_csv("./prevalence/depression/clean/22-24-juin.csv", encoding="utf-8")
depression_0810juin_df = pd.read_csv("./prevalence/depression/clean/8-10-juin.csv", encoding="utf-8")
depression_2729mai_df = pd.read_csv("./prevalence/depression/clean/27-29-mai.csv", encoding="utf-8")
depression_1820mai_df = pd.read_csv("./prevalence/depression/clean/18-20-mai.csv", encoding="utf-8")
depression_1315mai_df = pd.read_csv("./prevalence/depression/clean/13-15-mai.csv", encoding="utf-8")
depression_0406mai_df = pd.read_csv("./prevalence/depression/clean/04-06-mai.csv", encoding="utf-8")
depression_2830avril_df = pd.read_csv("./prevalence/depression/clean/28-30-avril.csv", encoding="utf-8")
depression_2022avril_df = pd.read_csv("./prevalence/depression/clean/20-22-avril.csv", encoding="utf-8")
depression_1416avril_df = pd.read_csv("./prevalence/depression/clean/14-16-avril.csv", encoding="utf-8")
depression_30mars_01avr_df = pd.read_csv("./prevalence/depression/clean/30-mars-01-avril.csv", encoding="utf-8")
depression_df = [depression_2022juillet_df, depression_0608juillet_df, depression_2224juin_df, depression_0810juin_df, depression_2729mai_df,depression_1820mai_df,
            depression_1315mai_df,depression_0406mai_df, depression_2830avril_df, depression_2022avril_df ,depression_1416avril_df,depression_30mars_01avr_df ]
# Sleep problem datasets
sleep_2022juillet_df = pd.read_csv("./prevalence/pb_sommeil/clean/20-22-juillet.csv", encoding="utf-8")
sleep_0608juillet_df = pd.read_csv("./prevalence/pb_sommeil/clean/6-8-juillet.csv", encoding="utf-8")
sleep_2224juin_df = pd.read_csv("./prevalence/pb_sommeil/clean/22-24-juin.csv", encoding="utf-8")
sleep_0810juin_df = pd.read_csv("./prevalence/pb_sommeil/clean/8-10-juin.csv", encoding="utf-8")
sleep_2729mai_df = pd.read_csv("./prevalence/pb_sommeil/clean/27-29-mai.csv", encoding="utf-8")
sleep_1820mai_df = pd.read_csv("./prevalence/pb_sommeil/clean/18-20-mai.csv", encoding="utf-8")
sleep_1315mai_df = pd.read_csv("./prevalence/pb_sommeil/clean/13-15-mai.csv", encoding="utf-8")
sleep_0406mai_df = pd.read_csv("./prevalence/pb_sommeil/clean/04-06-mai.csv", encoding="utf-8")
sleep_2830avril_df = pd.read_csv("./prevalence/pb_sommeil/clean/28-30-avril.csv", encoding="utf-8")
sleep_2022avril_df = pd.read_csv("./prevalence/pb_sommeil/clean/20-22-avril.csv", encoding="utf-8")
sleep_1416avril_df = pd.read_csv("./prevalence/pb_sommeil/clean/14-16-avril.csv", encoding="utf-8")
sleep_30mars_01avr_df = pd.read_csv("./prevalence/pb_sommeil/clean/30-mars-01-avril.csv", encoding="utf-8")
sleep_df = [sleep_2022juillet_df, sleep_0608juillet_df, sleep_2224juin_df, sleep_0810juin_df, sleep_2729mai_df,sleep_1820mai_df,
            sleep_1315mai_df, sleep_0406mai_df, sleep_2830avril_df, sleep_2022avril_df ,sleep_1416avril_df,sleep_30mars_01avr_df ]
# hygene measures datasets
hygene_2022juillet_df = pd.read_csv("./prevalence/hygene/clean/20-22-juillet.csv", encoding="utf-8")
hygene_0608juillet_df = pd.read_csv("./prevalence/hygene/clean/06-08-juillet.csv", encoding="utf-8")
hygene_2224juin_df = pd.read_csv("./prevalence/hygene/clean/22-24-juin.csv", encoding="utf-8")
hygene_0810juin_df = pd.read_csv("./prevalence/hygene/clean/8-10-juin.csv", encoding="utf-8")
hygene_2729mai_df = pd.read_csv("./prevalence/hygene/clean/27-29-mai.csv", encoding="utf-8")
hygene_1820mai_df = pd.read_csv("./prevalence/hygene/clean/18-20-mai.csv", encoding="utf-8")
hygene_1315mai_df = pd.read_csv("./prevalence/hygene/clean/13-15-mai.csv", encoding="utf-8")
hygene_0406mai_df = pd.read_csv("./prevalence/hygene/clean/04-06-mai.csv", encoding="utf-8")
hygene_2830avril_df = pd.read_csv("./prevalence/hygene/clean/28-30-avril.csv", encoding="utf-8")
hygene_2022avril_df = pd.read_csv("./prevalence/hygene/clean/20-22-avril.csv", encoding="utf-8")
hygene_1416avril_df = pd.read_csv("./prevalence/hygene/clean/14-16-avril.csv", encoding="utf-8")
hygene_30mars_01avr_df = pd.read_csv("./prevalence/hygene/clean/30-mars-01-avril.csv", encoding="utf-8")
hygene_df = [hygene_2022juillet_df, hygene_0608juillet_df, hygene_2224juin_df, hygene_0810juin_df, hygene_2729mai_df,hygene_1820mai_df,
            hygene_1315mai_df, hygene_0406mai_df, hygene_2830avril_df, hygene_2022avril_df , hygene_1416avril_df, hygene_30mars_01avr_df ]
# masks datasets
masks_2022juillet_df = pd.read_csv("./prevalence/masks/clean/20-22-juillet.csv", encoding="utf-8")
masks_0608juillet_df = pd.read_csv("./prevalence/masks/clean/6-8-juillet.csv", encoding="utf-8")
masks_2224juin_df = pd.read_csv("./prevalence/masks/clean/22-24-juin.csv", encoding="utf-8")
masks_0810juin_df = pd.read_csv("./prevalence/masks/clean/08-10-juin.csv", encoding="utf-8")
masks_2729mai_df = pd.read_csv("./prevalence/masks/clean/27-29-mai.csv", encoding="utf-8")
masks_1820mai_df = pd.read_csv("./prevalence/masks/clean/18-20-mai.csv", encoding="utf-8")
masks_1315mai_df = pd.read_csv("./prevalence/masks/clean/13-15-mai.csv", encoding="utf-8")
masks_0406mai_df = pd.read_csv("./prevalence/masks/clean/04-06-mai.csv", encoding="utf-8")
masks_2830avril_df = pd.read_csv("./prevalence/masks/clean/28-30-avril.csv", encoding="utf-8")
masks_2022avril_df = pd.read_csv("./prevalence/masks/clean/20-22-avril.csv", encoding="utf-8")
masks_1416avril_df = pd.read_csv("./prevalence/masks/clean/14-16-avril.csv", encoding="utf-8")
masks_30mars_01avr_df = pd.read_csv("./prevalence/masks/clean/30-mars-01-avril.csv", encoding="utf-8")
masks_df = [masks_2022juillet_df, masks_0608juillet_df, masks_2224juin_df, masks_0810juin_df, masks_2729mai_df,masks_1820mai_df,
            masks_1315mai_df,masks_0406mai_df, masks_2830avril_df, masks_2022avril_df ,masks_1416avril_df,masks_30mars_01avr_df ]
# adoption of the 4 hygene measures datasets
hygene4_2022juillet_df = pd.read_csv("./prevalence/adoption_hygene/clean/20-22-juillet.csv", encoding="utf-8")
hygene4_0608juillet_df = pd.read_csv("./prevalence/adoption_hygene/clean/6-8-juillet.csv", encoding="utf-8")
hygene4_2224juin_df = pd.read_csv("./prevalence/adoption_hygene/clean/22-24-juillet.csv", encoding="utf-8")
hygene4_0810juin_df = pd.read_csv("./prevalence/adoption_hygene/clean/8-10-juin.csv", encoding="utf-8")
hygene4_2729mai_df = pd.read_csv("./prevalence/adoption_hygene/clean/27-29-mai.csv", encoding="utf-8")
hygene4_1820mai_df = pd.read_csv("./prevalence/adoption_hygene/clean/18-20-mai.csv", encoding="utf-8")
hygene4_1315mai_df = pd.read_csv("./prevalence/adoption_hygene/clean/13-15-mai.csv", encoding="utf-8")
hygene4_0406mai_df = pd.read_csv("./prevalence/adoption_hygene/clean/04-06-mai.csv", encoding="utf-8")
hygene4_2830avril_df = pd.read_csv("./prevalence/adoption_hygene/clean/28-30-avril.csv", encoding="utf-8")
hygene4_2022avril_df = pd.read_csv("./prevalence/adoption_hygene/clean/20-22-juillet.csv", encoding="utf-8")
hygene4_1416avril_df = pd.read_csv("./prevalence/adoption_hygene/clean/14-16-avril.csv", encoding="utf-8")
hygene4_30mars_01avr_df = pd.read_csv("./prevalence/adoption_hygene/clean/30-mars-1-avril.csv", encoding="utf-8")
hygene4_df = [hygene4_2022juillet_df, hygene4_0608juillet_df, hygene4_2224juin_df, hygene4_0810juin_df, hygene4_2729mai_df,hygene4_1820mai_df,
            hygene4_1315mai_df,hygene4_0406mai_df, hygene4_2830avril_df, hygene4_2022avril_df ,hygene4_1416avril_df,hygene4_30mars_01avr_df ]
preval_dfs = [anxiety_df ,
                depression_df,
                sleep_df,
                hygene_df ,
                masks_df,
                hygene4_df]
total_pop = 66000000
initial_infected = 7412
initial_recovered = 2056
recovery_rate = 14
reproduction_rate = 6
t = 100

# dataset after confinement and start of hygienic measures
mask_conf = (agg_day_df['jour'] >= "2020-05-11") & (agg_day_df['jour']<="2020-07-20")
df_decon = agg_day_df[mask_conf]
# dataset after mask obligation
mask_mask = agg_day_df['jour'] > "2020-07-20"
df_mask = agg_day_df[mask_mask]
# dataset of confinement period
mask_conf = agg_day_df['jour'] < "2020-05-11"
df_conf = agg_day_df[mask_conf]
# Traces to plot regional data (Death and Recovery)
trace1 = go.Bar(
    x=agg_reg['reg'],
    y=agg_reg['rad'],
    name = 'Recover',
    marker=dict(color='royalblue'), # set the marker color
    #hoverinfo='y'
)
trace2 = go.Bar(
    x=agg_reg['reg'],
    y=agg_reg['dc'],
    name='Death',
    marker=dict(color='firebrick'),
    #hoverinfo='y'
)

data = [trace2,trace1]
layout = go.Layout(
    title='Overall Recovery/Death per regions',
    barmode='stack',
    yaxis={'title':'Number of people'}
)
end_confinement = "2020-05-11"
start_mask = "2020-07-20"
eval_fig = go.Figure()
eval_fig.add_trace(go.Bar(
                        x=agg_day_df['jour'],
                        y=agg_day_df['incid_dc'],
                        name='Death',
                        marker=dict(color='firebrick')))
eval_fig.add_trace(go.Bar(
                        x=agg_day_df['jour'],
                        y=agg_day_df['incid_rad'],
                        name='Recovery',

                        marker=dict(color='royalblue')))
eval_fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=end_confinement, # End of confinement
            y0=0,
            x1=end_confinement,
            y1=agg_day_df['incid_rad'].max(),
            line=dict(color="black",
                      width=3)))
eval_fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=start_mask, # Start date of mask obligation
            y0=0,
            x1=start_mask,
            y1=agg_day_df['incid_rad'].max(),
            line=dict(color="black",
                      width=3)))
eval_fig.add_trace(go.Scatter(
    x=[end_confinement, start_mask],
    y=[agg_day_df['incid_rad'].max(), agg_day_df['incid_rad'].max()],
    text=["End of confinement and obligation of social distancing and hygienic measures",
          "Start date of mask obligation plus social distancing and hygienic measures"],
    mode="text",
    name='Events'
))

# Statistics of Death after mask obligations
eval_fig.add_trace(go.Scatter(
    x=["2020-07-30","2020-07-30","2020-07-30","2020-07-30","2020-07-30"],
    y=[2000, 1800, 1600, 1400, 1200],
    text=['DEATH \n',
            "Max : {}".format(df_mask['incid_dc'].max()),
            "Min : {}".format(df_mask['incid_dc'].min()),
            "Mean : {}".format(round(df_mask['incid_dc'].mean(),2)),
            "Total : {}".format(df_mask['incid_dc'].sum())],
    mode="text",
    name = "Death during mask obligation"

))

# Statistics of Recovery after mask obligatons
eval_fig.add_trace(go.Scatter(
    x=["2020-08-18","2020-08-18","2020-08-18","2020-08-18","2020-08-18"],
    y=[2000, 1800, 1600, 1400, 1200],
    text=['Recovery \n',
            "Max : {}".format(df_mask['incid_rad'].max()),
            "Min : {}".format(df_mask['incid_rad'].min()),
            "Mean : {}".format(round(df_mask['incid_rad'].mean(),2)),
            "Total : {}".format(df_mask['incid_rad'].sum())],
    mode="text",
    name = "Recovery during mask obligation"

))

# Statistics of Death after confinement
eval_fig.add_trace(go.Scatter(
    x=["2020-05-28","2020-05-28","2020-05-28","2020-05-28","2020-05-28"],
    y=[2000, 1800, 1600, 1400, 1200],
    text=['DEATH \n',
            "Max : {}".format(df_decon['incid_dc'].max()),
            "Min : {}".format(df_decon['incid_dc'].min()),
            "Mean : {}".format(round(df_decon['incid_dc'].mean(),2)),
            "Total : {}".format(df_decon['incid_dc'].sum())],
    mode="text",
    name='Death after confinement'

))

# Statistics of Recovery after confinement
eval_fig.add_trace(go.Scatter(
    x=["2020-06-12","2020-06-12","2020-06-12","2020-06-12","2020-06-12"],
    y=[2000, 1800, 1600, 1400, 1200],
    text=['Recovery \n',
            "Max : {}".format(df_decon['incid_rad'].max()),
            "Min : {}".format(df_decon['incid_rad'].min()),
            "Mean : {}".format(round(df_decon['incid_rad'].mean(),2)),
            "Total : {}".format(df_decon['incid_rad'].sum())],
    mode="text",
    name='Recovery after Confinement'

))

# Statistics of Death during confinement
eval_fig.add_trace(go.Scatter(
    x=["2020-03-9","2020-03-9","2020-03-9","2020-03-9","2020-03-9"],
    y=[2000, 1800, 1600, 1400, 1200],
    text=['DEATH \n',
            "Max : {}".format(df_conf['incid_dc'].max()),
            "Min : {}".format(df_conf['incid_dc'].min()),
            "Mean : {}".format(round(df_conf['incid_dc'].mean(),2)),
            "Total : {}".format(df_conf['incid_dc'].sum())],
    mode="text",
    name='Death during confinement'

))

# Statistics of Recovery during confinement
eval_fig.add_trace(go.Scatter(
    x=["2020-03-23","2020-03-23","2020-03-23","2020-03-23","2020-03-23"],
    y=[2000, 1800, 1600, 1400, 1200],
    text=['Recovery \n',
            "Max : {}".format(df_conf['incid_rad'].max()),
            "Min : {}".format(df_conf['incid_rad'].min()),
            "Mean : {}".format(round(df_conf['incid_rad'].mean(),2)),
            "Total : {}".format(df_conf['incid_rad'].sum())],
    mode="text",
    name='Recovery during confinement'

))
eval_fig.update_layout(
            title='COVID-19 Death/ Recovery daily count between {} and {} '.format(agg_day_df['jour'].min(), agg_day_df['jour'].max()),
            xaxis_title='Day',
            yaxis_title='Number of people')



# This code was taken from: https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/
# All credit should go to this website
def SIR(total_pop, inital_infected, initial_recovered, recovery_rate, reproduction_rate, t):
    # Total population, N.
    N = total_pop
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, R0 = inital_infected, initial_recovered
    # Reproduction Rate (5.7 w/o social distancing, 1.5 w social distancing)
    r0 = reproduction_rate
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0
    # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
    gamma = 1.0 / recovery_rate
    beta = gamma * r0

    # The SIR model differential equations.
    def deriv(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    # A grid of time points (in days)
    t = np.linspace(0, t, t)

    # Initial conditions vector
    y0 = S0, I0, R0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    return S, I, R, gamma, beta

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(
    [
        dcc.Tabs(id="tabs-example",
                value='tab-3-example',
                children=[
                dcc.Tab(label='GEO Hospital data',
                        value='tab-3-example',
                        children=[
                        html.Div([
                            html.H4('Select data to visualise', style={'marginLeft':10, 'paddingTop':10, 'paddingBottom':5}),
                            dcc.Dropdown(
                                id='geo_data_dropdown',
                                options=[{'label': i, 'value': i} for i in geo_labels],
                                value=geo_labels[0],
                                style={'marginLeft':5, 'width':'900px'}),
                            html.Div(id='geo_data_vis')
                        ],style=dict(float='left')),
                        html.Div([
                            dcc.Graph(
                                style=dict(paddingTop=30, height=400),
                                id='Stack Bar',
                                figure={
                                    'data': data,
                                    'layout': layout})
                        ],style=dict(float='right', width=900)),
                        html.Div([
                            html.Div([
                                html.H2('Confirmed Cases'),
                                html.H2(267077),
                            ],style=dict(float='left', width='40%')),
                            html.Div([
                                html.H2('Recovered'),
                                html.H2(86177),
                            ],style=dict(float='left', width='25%')),
                            html.Div([
                                html.H2('Death'),
                                html.H2(30596),
                            ],style=dict(float='right', width='25%'))
                        ], style=dict(width=850, float='right', marginTop=50))]),
                dcc.Tab(label='SIR Analysis',
                        value='tab-2-example',
                        children=[
                        #dbc.Row([
                        html.Div([
                            html.P('Select reproduction rate', style=dict(marginLeft=20, marginTop=10)),
                            dcc.Slider(
                                id='reprod_rate',
                                min=1,
                                max=30,
                                value=5,
                                step=1,
                                marks={i: str(i) for i in range(1, 31)}),
                            html.P('Select Duration of study', style=dict(marginLeft=20, marginTop=10)),
                            dcc.Slider(
                                id='sir_duration',
                                min=1,
                                max=100,
                                value=50,
                                step=1,
                                marks={i: str(i) for i in range(1, 101)}),
                            dcc.RadioItems(
                                id='sir_radio',
                                options=[{'label': i, 'value': i} for i in sir_labels],
                                value=sir_labels[0],
                                labelStyle={"margin-right": "20px"},
                                style=dict(marginLeft=20, marginTop=10, marginRight=30)
                            ),
                            html.Button(children='Run SIR Model', n_clicks = 0, id='run_sir',style={'marginLeft':'20px', "marginBottom":"5px"}),
                        ]),
                        dbc.Row([]),

                        html.Div(id='sir_vis')
                        ]),
                dcc.Tab(label='Geo Prevalence data',
                        value='tab-4-example',
                        children=[
                        html.Div([
                            html.H4('Select data to visualise', style={'marginLeft':10, 'paddingTop':10, 'paddingBottom':5}),
                            dcc.Dropdown(
                                id='preval_data_dropdown',
                                options=[{'label': i, 'value': i} for i in preval_labels],
                                value=preval_labels[0],
                                style={'marginLeft':5, 'width':'900px'}),
                            html.Div(id='preval_data_vis')
                        ])
                        ]),
                dcc.Tab(label='Prevalence Info',
                        value='tab-5-example',
                        children=[
                        html.Div([
                            html.H2('Select indicator to visualize'),
                            dcc.RadioItems(
                                id='preval_radio',
                                options=[{'label': i, 'value': i} for i in preval_labels],
                                value=preval_labels[0],
                                labelStyle={"margin-right": "15px", 'display': 'block'},
                                style=dict(marginLeft=20, marginTop=10, marginRight=30)
                            ),
                            html.H2('Select period'),
                            dcc.Dropdown(
                                id='my_preval_data_dropdown',
                                options=[{'label': i, 'value': i} for i in preval_drop_labels],
                                value=preval_drop_labels[0],
                                style={'marginLeft':10, 'width':'200px'}),
                            html.Div(id='preval_mapping_output',style=dict(width=850, float='left', marginTop=50)),
                            html.Div(id='preval_description',style=dict(width=850, float='right', marginTop=50))])]),
                dcc.Tab(label = "Evaluation",
                        value='evaluation-tab',
                        children=[
                            html.Div([
                                dcc.Graph(figure=eval_fig)])])])]
)

# Provide more information about the prevalence
@app.callback(
    Output(component_id='preval_description', component_property='children'),
    [Input(component_id='preval_radio',component_property='value')]
)
def preval_desc_handler(radio):

    if radio == preval_labels[0]:
        tooltip = html.Div(children =[
                                    html.B('Source'),
                                    html.P("Santé publique France - Enquête CoviPrev"),
                                    html.B('Unite'),
                                    html.P('%'),
                                    html.B("Description : "),
                                    html.P("Prévalences et évolutions régionales de l’anxiété pendant l’épidémie de Covid-19 (% ; données pondérées)."),
                                    html.B("Précisions :"),
                                    html.P("L’anxiété est mesurée par l’échelle HAD:Hospitality Anxiety and Depression scale ; score > 10. \
                                            Un intervalle de confiance à 95% est indiqué. Les classes sont calculées avec la méthodes des quantiles."),
                                    html.B("Limites : "),
                                    html.P("Données déclaratives, sujettes à un biais de déclaration. Pour certaines régions, les effectifs \
                                            peuvent être assez faibles (~100 répondants), conduisant à une incertitude dans les estimations produites."),
                                    html.A('En savoir +',target='_blank', href='https://www.santepubliquefrance.fr/etudes-et-enquetes/covid-19-une-enquete-pour-suivre-l-evolution-des-comportements-et-de-la-sante-mentale-pendant-le-confinement')
                                ]),
    elif radio == preval_labels[1]:
        tooltip = html.Div(children =[
                                    html.B('Source'),
                                    html.P("Santé publique France - Enquête CoviPrev"),
                                    html.B('Unite'),
                                    html.P('%'),
                                    html.B("Description : "),
                                    html.P("Prévalences et évolutions régionales de la dépression face à l’épidémie de Covid-19 (% ; données pondérées)."),
                                    html.B("Précisions :"),
                                    html.P("L’anxiété est mesurée par l’échelle HAD:Hospitality Anxiety and Depression scale ; score > 10. \
                                            Un intervalle de confiance à 95% est indiqué. Les classes sont calculées avec la méthodes des quantiles."),
                                    html.B("Limites : "),
                                    html.P("Données déclaratives, sujettes à un biais de déclaration. Pour certaines régions, les effectifs \
                                            peuvent être assez faibles (~100 répondants), conduisant à une incertitude dans les estimations produites."),
                                    html.A('En savoir +',target='_blank', href='https://www.santepubliquefrance.fr/etudes-et-enquetes/covid-19-une-enquete-pour-suivre-l-evolution-des-comportements-et-de-la-sante-mentale-pendant-le-confinement')
                                ]),
    elif radio == preval_labels[2]:
        tooltip = html.Div(children =[
                                    html.B('Source'),
                                    html.P("Santé publique France - Enquête CoviPrev"),
                                    html.B("Description : "),
                                    html.P("Prévalences et évolutions régionales des problèmes de sommeil face à l’épidémie de Covid-19 (% ; données pondérées)"),
                                    html.B("Précisions :"),
                                    html.P("La question posée était « Diriez-vous qu’au cours des 8 derniers jours, vous avez eu des problèmes de sommeil… ? ». \
                                            Les personnes ayant répondu 'un peu' ou 'beaucoup' à la question ont été considérées comme ayant des problèmes de sommeil. \
                                            Les prévalences sont associées à un intervalle de confiance à 95%. Les classes sont calculées avec la méthode des quantiles"),
                                    html.B("Limites : "),
                                    html.P("Données déclaratives, sujettes à un biais de déclaration. Pour certaines régions, les effectifs \
                                            peuvent être assez faibles (~100 répondants), conduisant à une incertitude dans les estimations produites."),
                                    html.A('En savoir +',target='_blank', href='https://www.santepubliquefrance.fr/etudes-et-enquetes/covid-19-une-enquete-pour-suivre-l-evolution-des-comportements-et-de-la-sante-mentale-pendant-le-confinement')
                                ]),
    elif radio == preval_labels[3]:
        tooltip = html.Div(children =[
                                    html.B('Source'),
                                    html.P("Santé publique France - Enquête CoviPrev"),
                                    html.B("Description : "),
                                    html.P("Nombre moyen et évolutions régionales des mesures d’hygiène systématiquement adoptées parmi les \
                                            4 mesures recommandées par les pouvoirs publics pendant l’épidémie de Covid-19 (moyennes ; données pondérées)."),
                                    html.B("Précisions :"),
                                    html.P("Les 4 mesures d’hygiène adoptées systématiquement : Se laver régulièrement les mains ; \
                                            Saluer sans serrer la main et arrêter les embrassades ; Tousser dans son coude ; Utiliser un mouchoir à usage unique"),
                                    html.B("Limites : "),
                                    html.P("Données déclaratives, sujettes à un biais de déclaration. Pour certaines régions, les effectifs \
                                            peuvent être assez faibles (~100 répondants), conduisant à une incertitude dans les estimations produites."),
                                    html.A('En savoir +',target='_blank', href='https://www.santepubliquefrance.fr/etudes-et-enquetes/covid-19-une-enquete-pour-suivre-l-evolution-des-comportements-et-de-la-sante-mentale-pendant-le-confinement')
                                ]),
    elif radio == preval_labels[4]:
        tooltip = html.Div(children =[
                                    html.B('Source'),
                                    html.P("Santé publique France - Enquête CoviPrev"),
                                    html.B("Description : "),
                                    html.P("Prévalences et évolutions régionales de l’adoption systématique du port du masque en public pendant l’épidémie de Covid-19 (% ; données pondérées)"),
                                    html.B("Précisions :"),
                                    html.P("La question posée était : « Au cours des derniers jours, avez-vous adopté la mesure ‘Porter un masque en public’ ? ». \
                                            N’ont été retenues que les personnes ayant déclaré adopter « systématiquement » cette mesure.\
                                            Les prévalences sont associées à un intervalle de confiance à 95%. Les classes sont calculées avec la méthode des quantiles."),
                                    html.B("Limites : "),
                                    html.P("Données déclaratives, sujettes à un biais de déclaration. Pour certaines régions, les effectifs \
                                            peuvent être assez faibles (~100 répondants), conduisant à une incertitude dans les estimations produites."),
                                    html.A('En savoir +',target='_blank', href='https://www.santepubliquefrance.fr/etudes-et-enquetes/covid-19-une-enquete-pour-suivre-l-evolution-des-comportements-et-de-la-sante-mentale-pendant-le-confinement')
                                ]),
    elif radio == preval_labels[5]:
        tooltip = html.Div(children =[
                                    html.B('Source'),
                                    html.P("Santé publique France - Enquête CoviPrev"),
                                    html.B("Description : "),
                                    html.P("Nombre moyen et évolutions régionales des mesures d’hygiène systématiquement adoptées parmi les \
                                            4 mesures recommandées par les pouvoirs publics pendant l’épidémie de Covid-19 (moyennes ; données pondérées)."),
                                    html.B("Précisions :"),
                                    html.P("Les 4 mesures d’hygiène adoptées systématiquement : Se laver régulièrement les mains ; Saluer sans serrer la main et arrêter les embrassades \
                                            ; Tousser dans son coude ; Utiliser un mouchoir à usage unique. \
                                            Les moyennes sont associées à un intervalle de confiance à 95%. Les classes sont calculées avec la méthode des quantiles."),
                                    html.B("Limites : "),
                                    html.P("Données déclaratives, sujettes à un biais de déclaration. Pour certaines régions, les effectifs \
                                            peuvent être assez faibles (~100 répondants), conduisant à une incertitude dans les estimations produites."),
                                    html.A('En savoir +',target='_blank', href='https://www.santepubliquefrance.fr/etudes-et-enquetes/covid-19-une-enquete-pour-suivre-l-evolution-des-comportements-et-de-la-sante-mentale-pendant-le-confinement')
                                ]),
    return tooltip


@app.callback(
    Output(component_id='preval_mapping_output', component_property='children'),
    [Input(component_id='my_preval_data_dropdown',component_property='value')],
    [State(component_id='preval_radio',component_property='value')]
)
def preval_handler(dropdown_val, radio_val):
    map = html.H2('Visual under development....')
    if radio_val == preval_labels[0]:
        if dropdown_val == preval_drop_labels[0]:
            # create traces using a list comprehension:
            data = [go.Bar(
                x = preval_dfs[0][0]['region'],
                y = preval_dfs[0][0][preval_dfs[0][0].columns[2]],
                name=response
            ) for response in [preval_dfs[0][0].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[0]+ " "+ preval_drop_labels[0],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[1]:
            data = [go.Bar(
                x = preval_dfs[0][1]['region'],
                y = preval_dfs[0][1][preval_dfs[0][1].columns[2]],
                name=response
            ) for response in [preval_dfs[0][1].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[0]+ " "+ preval_drop_labels[1],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[2]:
            data = [go.Bar(
                x = preval_dfs[0][2]['region'],
                y = preval_dfs[0][2][preval_dfs[0][2].columns[2]],
                name=response
            ) for response in [preval_dfs[0][2].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[0]+ " "+ preval_drop_labels[2],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[3]:
                        data = [go.Bar(
                            x = preval_dfs[0][3]['region'],
                            y = preval_dfs[0][3][preval_dfs[0][3].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][3].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[3],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[4]:
                        data = [go.Bar(
                            x = preval_dfs[0][4]['region'],
                            y = preval_dfs[0][4][preval_dfs[0][4].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][4].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[4],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[5]:
                        data = [go.Bar(
                            x = preval_dfs[0][5]['region'],
                            y = preval_dfs[0][5][preval_dfs[0][5].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][5].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[5],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[6]:
                        data = [go.Bar(
                            x = preval_dfs[0][6]['region'],
                            y = preval_dfs[0][6][preval_dfs[0][6].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][6].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[6],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[7]:
                        data = [go.Bar(
                            x = preval_dfs[0][7]['region'],
                            y = preval_dfs[0][7][preval_dfs[0][7].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][7].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[7],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[8]:
                        data = [go.Bar(
                            x = preval_dfs[0][8]['region'],
                            y = preval_dfs[0][8][preval_dfs[0][8].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][8].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[8],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[9]:

                        data = [go.Bar(
                            x = preval_dfs[0][9]['region'],
                            y = preval_dfs[0][9][preval_dfs[0][9].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][9].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[9],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[10]:
                        data = [go.Bar(
                            x = preval_dfs[0][10]['region'],
                            y = preval_dfs[0][10][preval_dfs[0][10].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][10].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[10],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[11]:
                        data = [go.Bar(
                            x = preval_dfs[0][11]['region'],
                            y = preval_dfs[0][11][preval_dfs[0][11].columns[2]],
                            name=response
                        ) for response in [preval_dfs[0][11].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[11],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
    elif radio_val == preval_labels[1]:
        if dropdown_val == preval_drop_labels[1]:
            # create traces using a list comprehension:
            data = [go.Bar(
                x = preval_dfs[1][0]['region'],
                y = preval_dfs[1][0][preval_dfs[1][0].columns[2]],
                name=response
            ) for response in [preval_dfs[0][0].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[1]+ " "+ preval_drop_labels[0],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[1]:
            data = [go.Bar(
                x = preval_dfs[1][1]['region'],
                y = preval_dfs[1][1][preval_dfs[1][1].columns[2]],
                name=response
            ) for response in [preval_dfs[0][1].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[1]+ " "+ preval_drop_labels[1],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[2]:
            data = [go.Bar(
                x = preval_dfs[1][2]['region'],
                y = preval_dfs[1][2][preval_dfs[1][2].columns[2]],
                name=response
            ) for response in [preval_dfs[1][2].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[1]+ " "+ preval_drop_labels[2],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[3]:
                        data = [go.Bar(
                            x = preval_dfs[1][3]['region'],
                            y = preval_dfs[1][3][preval_dfs[1][3].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][3].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[0]+ " "+ preval_drop_labels[3],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[4]:
                        data = [go.Bar(
                            x = preval_dfs[1][4]['region'],
                            y = preval_dfs[1][4][preval_dfs[1][4].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][4].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[1]+ " "+ preval_drop_labels[4],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[5]:
                        data = [go.Bar(
                            x = preval_dfs[1][5]['region'],
                            y = preval_dfs[1][5][preval_dfs[1][5].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][5].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[1]+ " "+ preval_drop_labels[5],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[6]:
                        data = [go.Bar(
                            x = preval_dfs[1][6]['region'],
                            y = preval_dfs[1][6][preval_dfs[1][6].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][6].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[1]+ " "+ preval_drop_labels[6],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[7]:
                        data = [go.Bar(
                            x = preval_dfs[1][7]['region'],
                            y = preval_dfs[1][7][preval_dfs[1][7].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][7].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[1]+ " "+ preval_drop_labels[7],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[8]:
                        data = [go.Bar(
                            x = preval_dfs[1][8]['region'],
                            y = preval_dfs[1][8][preval_dfs[1][8].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][8].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[1]+ " "+ preval_drop_labels[8],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[9]:

                        data = [go.Bar(
                            x = preval_dfs[1][9]['region'],
                            y = preval_dfs[1][9][preval_dfs[1][9].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][9].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[1]+ " "+ preval_drop_labels[9],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[10]:
                        data = [go.Bar(
                            x = preval_dfs[1][10]['region'],
                            y = preval_dfs[1][10][preval_dfs[1][10].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][10].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[1]+ " "+ preval_drop_labels[10],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[11]:
                        data = [go.Bar(
                            x = preval_dfs[1][11]['region'],
                            y = preval_dfs[1][11][preval_dfs[1][11].columns[2]],
                            name=response
                        ) for response in [preval_dfs[1][11].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[1]+ " "+ preval_drop_labels[11],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
    elif radio_val == preval_labels[2]:
        if dropdown_val == preval_drop_labels[0]:
            # create traces using a list comprehension:
            data = [go.Bar(
                x = preval_dfs[2][0]['region'],
                y = preval_dfs[2][0][preval_dfs[2][0].columns[2]],
                name=response
            ) for response in [preval_dfs[2][0].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[2]+ " "+ preval_drop_labels[0],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[1]:
            data = [go.Bar(
                x = preval_dfs[2][1]['region'],
                y = preval_dfs[2][1][preval_dfs[2][1].columns[2]],
                name=response
            ) for response in [preval_dfs[2][1].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[2]+ " "+ preval_drop_labels[1],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[2]:
            data = [go.Bar(
                x = preval_dfs[2][2]['region'],
                y = preval_dfs[2][2][preval_dfs[2][2].columns[2]],
                name=response
            ) for response in [preval_dfs[2][2].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[2]+ " "+ preval_drop_labels[2],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[3]:
                        data = [go.Bar(
                            x = preval_dfs[2][3]['region'],
                            y = preval_dfs[2][3][preval_dfs[2][3].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][3].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[3],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[4]:
                        data = [go.Bar(
                            x = preval_dfs[2][4]['region'],
                            y = preval_dfs[2][4][preval_dfs[2][4].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][4].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[4],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[5]:
                        data = [go.Bar(
                            x = preval_dfs[2][5]['region'],
                            y = preval_dfs[2][5][preval_dfs[2][5].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][5].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[5],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[6]:
                        data = [go.Bar(
                            x = preval_dfs[2][6]['region'],
                            y = preval_dfs[2][6][preval_dfs[2][6].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][6].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[6],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[7]:
                        data = [go.Bar(
                            x = preval_dfs[2][7]['region'],
                            y = preval_dfs[2][7][preval_dfs[2][7].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][7].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[7],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[8]:
                        data = [go.Bar(
                            x = preval_dfs[2][8]['region'],
                            y = preval_dfs[2][8][preval_dfs[2][8].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][8].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[8],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[9]:

                        data = [go.Bar(
                            x = preval_dfs[2][9]['region'],
                            y = preval_dfs[2][9][preval_dfs[0][9].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][9].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[9],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[10]:
                        data = [go.Bar(
                            x = preval_dfs[2][10]['region'],
                            y = preval_dfs[2][10][preval_dfs[2][10].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][10].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[10],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[11]:
                        data = [go.Bar(
                            x = preval_dfs[2][11]['region'],
                            y = preval_dfs[2][11][preval_dfs[2][11].columns[2]],
                            name=response
                        ) for response in [preval_dfs[2][11].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[2]+ " "+ preval_drop_labels[11],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
    elif radio_val == preval_labels[3]:
        if dropdown_val == preval_drop_labels[0]:
            # create traces using a list comprehension:
            data = [go.Bar(
                x = preval_dfs[3][0]['region'],
                y = preval_dfs[3][0][preval_dfs[3][0].columns[2]],
                name=response
            ) for response in [preval_dfs[3][0].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[3]+ " "+ preval_drop_labels[0],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[1]:
            data = [go.Bar(
                x = preval_dfs[3][1]['region'],
                y = preval_dfs[3][1][preval_dfs[3][1].columns[2]],
                name=response
            ) for response in [preval_dfs[3][1].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[3]+ " "+ preval_drop_labels[1],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[2]:
            data = [go.Bar(
                x = preval_dfs[3][2]['region'],
                y = preval_dfs[3][2][preval_dfs[3][2].columns[2]],
                name=response
            ) for response in [preval_dfs[3][2].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[3]+ " "+ preval_drop_labels[2],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[3]:
                        data = [go.Bar(
                            x = preval_dfs[3][3]['region'],
                            y = preval_dfs[3][3][preval_dfs[3][3].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][3].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[3],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[4]:
                        data = [go.Bar(
                            x = preval_dfs[3][4]['region'],
                            y = preval_dfs[3][4][preval_dfs[3][4].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][4].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[4],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[5]:
                        data = [go.Bar(
                            x = preval_dfs[3][5]['region'],
                            y = preval_dfs[3][5][preval_dfs[3][5].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][5].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[5],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[6]:
                        data = [go.Bar(
                            x = preval_dfs[3][6]['region'],
                            y = preval_dfs[3][6][preval_dfs[3][6].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][6].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[6],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[7]:
                        data = [go.Bar(
                            x = preval_dfs[3][7]['region'],
                            y = preval_dfs[3][7][preval_dfs[3][7].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][7].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[7],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[8]:
                        data = [go.Bar(
                            x = preval_dfs[3][8]['region'],
                            y = preval_dfs[3][8][preval_dfs[3][8].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][8].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[8],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[9]:

                        data = [go.Bar(
                            x = preval_dfs[3][9]['region'],
                            y = preval_dfs[3][9][preval_dfs[3][9].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][9].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[9],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[10]:
                        data = [go.Bar(
                            x = preval_dfs[3][10]['region'],
                            y = preval_dfs[3][10][preval_dfs[3][10].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][10].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[10],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[11]:
                        data = [go.Bar(
                            x = preval_dfs[3][11]['region'],
                            y = preval_dfs[3][11][preval_dfs[3][11].columns[2]],
                            name=response
                        ) for response in [preval_dfs[3][11].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[3]+ " "+ preval_drop_labels[11],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
    elif radio_val == preval_labels[4]:
        if dropdown_val == preval_drop_labels[0]:
            # create traces using a list comprehension:
            data = [go.Bar(
                x = preval_dfs[4][0]['region'],
                y = preval_dfs[4][0][preval_dfs[4][0].columns[2]],
                name=response
            ) for response in [preval_dfs[4][0].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[4]+ " "+ preval_drop_labels[0],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[1]:
            data = [go.Bar(
                x = preval_dfs[4][1]['region'],
                y = preval_dfs[4][1][preval_dfs[4][1].columns[2]],
                name=response
            ) for response in [preval_dfs[4][1].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[4]+ " "+ preval_drop_labels[1],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[2]:
            data = [go.Bar(
                x = preval_dfs[4][2]['region'],
                y = preval_dfs[4][2][preval_dfs[4][2].columns[2]],
                name=response
            ) for response in [preval_dfs[4][2].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[4]+ " "+ preval_drop_labels[2],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[3]:
                        data = [go.Bar(
                            x = preval_dfs[4][3]['region'],
                            y = preval_dfs[4][3][preval_dfs[4][3].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][3].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[3],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[4]:
                        data = [go.Bar(
                            x = preval_dfs[4][4]['region'],
                            y = preval_dfs[4][4][preval_dfs[4][4].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][4].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[4],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[5]:
                        data = [go.Bar(
                            x = preval_dfs[4][5]['region'],
                            y = preval_dfs[4][5][preval_dfs[4][5].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][5].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[5],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[6]:
                        data = [go.Bar(
                            x = preval_dfs[4][6]['region'],
                            y = preval_dfs[4][6][preval_dfs[4][6].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][6].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[6],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[7]:
                        data = [go.Bar(
                            x = preval_dfs[4][7]['region'],
                            y = preval_dfs[4][7][preval_dfs[4][7].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][7].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[7],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[8]:
                        data = [go.Bar(
                            x = preval_dfs[4][8]['region'],
                            y = preval_dfs[4][8][preval_dfs[4][8].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][8].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[8],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[9]:

                        data = [go.Bar(
                            x = preval_dfs[4][9]['region'],
                            y = preval_dfs[4][9][preval_dfs[4][9].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][9].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[9],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[10]:
                        data = [go.Bar(
                            x = preval_dfs[4][10]['region'],
                            y = preval_dfs[4][10][preval_dfs[4][10].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][10].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[10],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[11]:
                        data = [go.Bar(
                            x = preval_dfs[4][11]['region'],
                            y = preval_dfs[4][11][preval_dfs[4][11].columns[2]],
                            name=response
                        ) for response in [preval_dfs[4][11].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[4]+ " "+ preval_drop_labels[11],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
    elif radio_val == preval_labels[5]:
        if dropdown_val == preval_drop_labels[0]:
            # create traces using a list comprehension:
            data = [go.Bar(
                x = preval_dfs[5][0]['region'],
                y = preval_dfs[5][0][preval_dfs[5][0].columns[2]],
                name=response
            ) for response in [preval_dfs[5][0].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[5]+ " "+ preval_drop_labels[0],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[1]:
            data = [go.Bar(
                x = preval_dfs[5][1]['region'],
                y = preval_dfs[5][1][preval_dfs[5][1].columns[2]],
                name=response
            ) for response in [preval_dfs[5][1].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[5]+ " "+ preval_drop_labels[1],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[2]:
            data = [go.Bar(
                x = preval_dfs[5][2]['region'],
                y = preval_dfs[5][2][preval_dfs[5][2].columns[2]],
                name=response
            ) for response in [preval_dfs[5][2].columns[2]]]

            # create a layout, remember to set the barmode here
            layout = go.Layout(
                title= preval_labels[5]+ " "+ preval_drop_labels[2],

                xaxis_title='Region',
                yaxis_title='Prevalence percentage'
                #barmode='stack'
            )
            # create a fig from data & layout, and plot the fig
            fig = go.Figure(data=data, layout=layout)
            map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[3]:
                        data = [go.Bar(
                            x = preval_dfs[5][3]['region'],
                            y = preval_dfs[5][3][preval_dfs[5][3].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][3].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[3],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[4]:
                        data = [go.Bar(
                            x = preval_dfs[5][4]['region'],
                            y = preval_dfs[5][4][preval_dfs[5][4].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][4].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[4],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[5]:
                        data = [go.Bar(
                            x = preval_dfs[5][5]['region'],
                            y = preval_dfs[5][5][preval_dfs[5][5].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][5].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[5],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[6]:
                        data = [go.Bar(
                            x = preval_dfs[5][6]['region'],
                            y = preval_dfs[5][6][preval_dfs[5][6].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][6].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[6],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[7]:
                        data = [go.Bar(
                            x = preval_dfs[5][7]['region'],
                            y = preval_dfs[5][7][preval_dfs[5][7].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][7].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[7],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[8]:
                        data = [go.Bar(
                            x = preval_dfs[5][8]['region'],
                            y = preval_dfs[5][8][preval_dfs[5][8].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][8].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[8],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[9]:

                        data = [go.Bar(
                            x = preval_dfs[5][9]['region'],
                            y = preval_dfs[5][9][preval_dfs[5][9].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][9].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[9],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[10]:
                        data = [go.Bar(
                            x = preval_dfs[5][10]['region'],
                            y = preval_dfs[5][10][preval_dfs[5][10].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][10].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[10],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)
        elif dropdown_val == preval_drop_labels[11]:
                        data = [go.Bar(
                            x = preval_dfs[5][11]['region'],
                            y = preval_dfs[5][11][preval_dfs[5][11].columns[2]],
                            name=response
                        ) for response in [preval_dfs[5][11].columns[2]]]

                        # create a layout, remember to set the barmode here
                        layout = go.Layout(
                            title= preval_labels[5]+ " "+ preval_drop_labels[11],

                            xaxis_title='Region',
                            yaxis_title='Prevalence percentage'
                            #barmode='stack'
                        )
                        # create a fig from data & layout, and plot the fig
                        fig = go.Figure(data=data, layout=layout)
                        map = dcc.Graph(figure=fig)

    return map

@app.callback(
    Output(component_id='sir_vis', component_property='children'),
    [Input(component_id='run_sir',component_property='n_clicks')],
    [State(component_id='reprod_rate',component_property='value'),
    State(component_id='sir_duration',component_property='value'),
    State(component_id='sir_radio',component_property='value')]
)
def sir_radio_handler(clicks, reprod_rate,sir_duration,radio):
    if (clicks > 0):
        if radio == sir_labels[1]:
            return html.H4('Not yet available...', style=dict(marginLeft=20, color='red'))

        elif radio == sir_labels[0]:
            sir_fig = go.Figure()
            S,I,R,gamma,beta= SIR(total_pop, initial_infected, initial_recovered ,recovery_rate, reprod_rate ,sir_duration)
            T =  np.arange(0, t)
            sir_fig.add_trace(go.Scatter(x=T, y=S,
                                        line_color='royalblue',
                                        name="Susceptible",
                                        ))
            sir_fig.add_trace(go.Scatter(x=T, y=I,
                                        line_color='firebrick',
                                        name="Infectious",
                                        ))
            sir_fig.add_trace(go.Scatter(x=T, y=R,
                                        line_color='rgb(231,107,243)',
                                        name="Recovery",
                                        ))
            sir_fig.update_layout(title='Proportion of S.I.R during the Corona Virus\n period modeled using SIR with Beta={} and Gamma={}'.format(beta,gamma),
                       xaxis_title='Number of days (Period of study)',
                       yaxis_title='Number of people')
            return dcc.Graph(figure=sir_fig)


@app.callback(
    Output(component_id='preval_data_vis', component_property='children'),
    [Input(component_id='preval_data_dropdown',component_property='value')]
)
def prev_data_drop(label):
    iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_dpps_epidemie.anxiete&serie=12. 6-8 juillet&lang=fr&iframe=1',
                        style=dict(width="900px", height="800px", marginLeft=10))
    if label == preval_labels[0]:
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_dpps_epidemie.anxiete&serie=12. 6-8 juillet&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == preval_labels[1]:
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_dpps_epidemie.depression&serie=13. 20-22 juillet&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == preval_labels[2]:
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_dpps_epidemie.pbsommeil&serie=13. 20-22 juillet&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == preval_labels[3]:
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_dpps_epidemie.nbmoy4mes&serie=13. 20-22 juillet&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == preval_labels[4]:
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_dpps_epidemie.portmasque&serie=13. 20-22 juillet&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == preval_labels[5]:
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_dpps_epidemie.hyg4mes&serie=13. 20-22 juillet&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == "":
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_dpps_epidemie.anxiete&serie=12. 6-8 juillet&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    return iframe



@app.callback(
    Output(component_id='geo_data_vis', component_property='children'),
    [Input(component_id='geo_data_dropdown',component_property='value')]
)
def geo_data_drop(label):
    iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit.dc&serie=2020-08-27&f1code=0&lang=fr&iframe=1',
                       style=dict(width="900px", height="800px", marginLeft=10))
    if label == geo_labels[0]:
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit.dc&serie=2020-08-27&f1code=0&lang=fr&iframe=1',
                           style=dict(width="900px", height="800px", marginLeft=10))
    elif label == geo_labels[1]:
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit.hosp&serie=2020-08-27&f1code=0&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == geo_labels[2]:
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit_incid.incid_rad&serie=2020-08-25&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == geo_labels[3]:
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit_incid.incid_dc&serie=2020-08-25&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == geo_labels[4]:
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit_incid.incid_rea&serie=2020-08-25&lang=fr&iframe=1',
                            style=dict(width="900px", height="800px", marginLeft=10))
    elif label == geo_labels[5]:
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit_incid.incid_hosp&serie=2020-08-25&lang=fr&iframe=1'
                            ,style=dict(width="900px", height="800px", marginLeft=10))
    elif label == geo_labels[6]:
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit.rea&serie=2020-08-27&f1code=0&lang=fr&iframe=1'
                            ,style=dict(width="1000px", height="800px", marginLeft=10))
    elif label == geo_labels[7]:
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit.rad&serie=2020-08-27&f1code=0&lang=fr&iframe=1'
                            ,style=dict(width="1000px", height="800px", marginLeft=10))
    elif label == "":
        print(label)
        iframe = html.Iframe(src='https://geodes.santepubliquefrance.fr/index.php?view=map1&indics=covid_hospit.dc&serie=2020-08-27&f1code=0&lang=fr&iframe=1',
                           style=dict(width="1000px", height="800px", marginLeft=10))
    return iframe


if __name__ == "__main__":
    app.run_server(debug=True, port=5000)
