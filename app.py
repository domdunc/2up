import pandas as pd
import numpy as np
import sys
import streamlit as st


number_of_games = st.sidebar.number_input('number of events', min_value=2, value=1000)
lay_commission = st.sidebar.number_input('lay commission', min_value=0)
fta_odds = st.sidebar.number_input('FTA odds', min_value=1.0, value=61.0)
back_odds = st.sidebar.number_input('back odds', min_value=0.01, value=2.60)
back_stake = st.sidebar.number_input('back stake', min_value=1.00, value=50.00)
lay_odds = st.sidebar.number_input('lay odds', min_value=0.01, value=2.66)
lay_stake = st.sidebar.number_input('lay stake', min_value=1.00, value=49.06)

back_win_amount = np.round((back_odds - 1) * back_stake, 2)
lay_win_amount = np.round(lay_stake * (1.0 - lay_commission), 2)
lay_liability = np.round((lay_odds - 1) * lay_stake, 2)
back_win_ql = np.round(abs(back_win_amount - lay_liability), 2)
lay_win_ql = np.round(abs(lay_win_amount - back_stake), 2)

avg_ql = (back_win_ql + lay_win_ql) / 2
fta_amount = back_win_amount + lay_win_amount


st.title('2UPs')

st.text(f"Back Win: {back_win_amount}\nLay Win: {lay_win_amount}\nLay Liability: {lay_liability}\nBack QL: {back_win_ql}\nLay QL: {lay_win_ql}\nFTA win: {fta_amount}")


# p = 1 / fta_odds
st.text('{}'.format(fta_odds))

win_sums = []
loss_sums = []
non_fta = 0
fta = 0

for t in range(number_of_games):
    if t % 10000 == 0:
        print(".", end='', flush=True)
    outcome = np.random.randint(1, fta_odds + 1)
    if outcome == 1:
        win_sums.append(fta_amount)
        loss_sums.append(0)
        fta += 1
    else:
        loss_sums.append(avg_ql)
        win_sums.append(0)
        non_fta += 1

pct_non_fta = (non_fta / number_of_games) * 100
pct_fta = (fta / number_of_games) * 100


data = pd.DataFrame({'win_sums' : win_sums, 'loss_sums' : loss_sums})
data['profitable'] = data.win_sums > data.loss_sums

non_fta_pct = np.round((non_fta/number_of_games)*100, 2)
fta_pct = np.round((fta / number_of_games) * 100, 2)

total_win_amount = np.round(sum(win_sums), 2)
total_lose_amount = np.round(sum(loss_sums), 2)
total_profit_amount = np.round((total_win_amount - total_lose_amount), 2)

mean_win_amount = np.round(np.mean(win_sums), 2)
mean_lose_amount = np.round(np.mean(loss_sums), 2)
mean_profit_amount = np.round(mean_win_amount-mean_lose_amount, 2)

st.text(f"\n\nNon FTA games %: {non_fta_pct}\nFTA games %: {fta_pct}\n")
st.text(f"Total win amount: {total_win_amount} \nTotal lose amount: {total_lose_amount} \nTotal profit amount: {total_profit_amount}")
st.text(f"Avg win amount: {mean_win_amount} \nAvg lose amount: {mean_lose_amount} \nAvg profit amount: {mean_profit_amount}")
