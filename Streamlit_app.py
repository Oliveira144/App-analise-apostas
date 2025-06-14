import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Análise de Apostas", layout="centered")
st.title("📊 Aplicativo de Análise de Apostas Esportivas")

st.subheader("Inserir dados da partida")

# Entrada de dados
time_casa = st.text_input("Time da casa")
time_visitante = st.text_input("Time visitante")
odd_casa = st.number_input("Odd - Time da casa", min_value=1.01, step=0.01, format="%.2f")
odd_visitante = st.number_input("Odd - Time visitante", min_value=1.01, step=0.01, format="%.2f")
odd_empate = st.number_input("Odd - Empate", min_value=1.01, step=0.01, format="%.2f")

# Stake da aposta (valor total disponível)
stake = st.number_input("Stake disponível (R$)", min_value=1.0, value=100.0, step=1.0)

if st.button("Analisar aposta"):
    with st.spinner("Calculando..."):

        # 1. Cálculo das probabilidades implícitas das odds
        prob_casa = 1 / odd_casa
        prob_visitante = 1 / odd_visitante
        prob_empate = 1 / odd_empate
        soma_probs = prob_casa + prob_visitante + prob_empate

        # Ajuste para remover margem da casa (normalização)
        prob_casa_ajust = prob_casa / soma_probs
        prob_visitante_ajust = prob_visitante / soma_probs
        prob_empate_ajust = prob_empate / soma_probs

        # 2. Definir probabilidades estimadas (exemplo: você pode integrar ML futuramente)
        # Aqui usamos uma suposição simples apenas para simulação
        prob_estimadas = {
            "Time da casa": prob_casa_ajust + 0.05,
            "Empate": prob_empate_ajust,
            "Time visitante": prob_visitante_ajust - 0.05
        }

        # 3. Calcular Value Bet
        value_bets = {}
        for nome, prob_real in zip(
            ["Time da casa", "Empate", "Time visitante"],
            [prob_casa_ajust + 0.05, prob_empate_ajust, prob_visitante_ajust - 0.05]
        ):
            odd = {"Time da casa": odd_casa, "Empate": odd_empate, "Time visitante": odd_visitante}[nome]
            prob_impli = 1 / odd
            value = prob_real * odd - 1
            value_bets[nome] = {
                "Probabilidade estimada": round(prob_real * 100, 2),
                "Value bet": value > 0,
                "Valor esperado (%)": round(value * 100, 2),
                "Kelly (%)": round(((odd * prob_real - 1) / (odd - 1)) * 100, 2) if value > 0 else 0
            }

        # 4. Mostrar resultados
        st.markdown("### 🔍 Resultados da análise")

        df_result = pd.DataFrame(value_bets).T
        df_result["Aposta recomendada"] = df_result["Kelly (%)"].apply(
            lambda x: "✅ Sim (Aposte)" if x > 0 else "❌ Não"
        )
        df_result["Sugestão de valor (R$)"] = df_result["Kelly (%)"] * stake / 100
        st.dataframe(df_result.style.format({
            "Probabilidade estimada": "{:.2f}%",
            "Valor esperado (%)": "{:.2f}%",
            "Kelly (%)": "{:.2f}%",
            "Sugestão de valor (R$)": "R${:.2f}"
        }))

        st.success("✅ Análise concluída. Veja acima as recomendações.")
