import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy.integrate import odeint


BASE = './data/27-08_2020/'
AGGREG=BASE+'/aggreg/'
INPUT = AGGREG+'agg_data_per_days.csv'
OUTPUT = AGGREG+'sir_per_day.csv'


df = pd.read_csv(INPUT)
df['I'] = df['incid_hosp'] + df['incid_rea']
df['R'] = df['incid_rad'] + df['incid_dc']

df_sir = df[['jour', 'I','R']]
df_sir['S'] = 66000000

for index in df_sir.index:
    if index == df_sir.index.min():
        df_sir.loc[index, 'S'] = 66000000 - (df_sir.loc[index, 'I'] + df_sir.loc[index, 'R'])
    elif(index < df_sir.index.max()):
        df_sir.loc[index, 'S'] = df_sir.loc[index-1, 'S'] - (df_sir.loc[index, 'I'] + df_sir.loc[index, 'R'])
df_sir.sort_values('jour', inplace=True)
df_sir.to_csv(OUTPUT,index=False)

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
