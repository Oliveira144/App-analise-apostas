import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise de Apostas", layout="centered")

st.title("📊 Aplicativo de Análise de Apostas Esportivas")

st.header("Inserir dados da partida")
time_casa = st.text_input("Time da casa")
time_fora = st.text_input("Time visitante")
odd_casa = st.number_input("Odd - Time da casa", min_value=1.01, value=1.80)
odd_fora = st.number_input("Odd - Time visitante", min_value=1.01, value=2.20)
odd_empate = st.number_input("Odd - Empate", min_value=1.01, value=3.30)

st.header("📈 Análise de Valor Esperado (Simples)")
prob_casa = 1 / odd_casa
prob_fora = 1 / odd_fora
prob_empate = 1 / odd_empate
prob_total = prob_casa + prob_fora + prob_empate

prob_casa /= prob_total
prob_fora /= prob_total
prob_empate /= prob_total

st.write("Probabilidades implícitas:")
st.write(f"🏠 {time_casa}: {prob_casa:.2%}")
st.write(f"🆚 Empate: {prob_empate:.2%}")
st.write(f"🚩 {time_fora}: {prob_fora:.2%}")

stake = st.number_input("Valor da aposta (stake)", value=100.0)

ve_casa = (odd_casa * prob_casa - 1) * stake
ve_empate = (odd_empate * prob_empate - 1) * stake
ve_fora = (odd_fora * prob_fora - 1) * stake

st.subheader("💰 Valor Esperado por Aposta")
st.write(f"🏠 {time_casa}: R$ {ve_casa:.2f}")
st.write(f"🆚 Empate: R$ {ve_empate:.2f}")
st.write(f"🚩 {time_fora}: R$ {ve_fora:.2f}")

melhor_valor = max(ve_casa, ve_empate, ve_fora)
if melhor_valor == ve_casa:
    st.success(f"Aposta recomendada: {time_casa}")
elif melhor_valor == ve_empate:
    st.success("Aposta recomendada: Empate")
else:
    st.success(f"Aposta recomendada: {time_fora}")
