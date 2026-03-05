# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:41:56 2026

@author: Henery Garção
"""

# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from utils.data_loader import carregar_dados

st.title("🧪 Práticas de Laboratório")

dados = carregar_dados()

if "PRÁTICAS" not in dados and "PRATICAS" not in dados:
    st.error("A aba PRÁTICAS não foi encontrada.")
    st.stop()

df = dados.get("PRÁTICAS", dados.get("PRATICAS"))


# ---------------------------------------------------------
# SEPARA TABELAS POR LABORATÓRIO
# ---------------------------------------------------------

def separar_labs(df):

    labs = {}

    lab_atual = None
    linhas = []

    for _, row in df.iterrows():

        valor = row[0]

        if isinstance(valor, str):

            texto = valor.upper()

            if "LAB" in texto:

                if lab_atual and len(linhas) > 0:
                    labs[lab_atual] = pd.DataFrame(linhas)

                lab_atual = valor.strip()
                linhas = []
                continue

        if lab_atual:
            linhas.append(row)

    if lab_atual and len(linhas) > 0:
        labs[lab_atual] = pd.DataFrame(linhas)

    return labs


# ---------------------------------------------------------
# ORGANIZA TABELA
# ---------------------------------------------------------

def organizar_tabela(df):

    df = df.dropna(how="all")

    if len(df) < 2:
        return None

    # primeira linha vira cabeçalho
    header = df.iloc[0]

    df = df[1:]

    df.columns = [
        "MÊS",
        "DIA",
        "SEMANA",
        "TURMA",
        "PRÁTICA",
        "ACONTECEU"
    ]

    df = df.reset_index(drop=True)

    # remove linhas completamente vazias
    df = df.dropna(how="all")

    # NaN vira vazio
    df = df.fillna("")

    return df


# ---------------------------------------------------------
# PROCESSAMENTO
# ---------------------------------------------------------

labs = separar_labs(df)

if len(labs) == 0:
    st.warning("Nenhuma tabela de práticas encontrada.")
    st.write(df.head(40))
    st.stop()


# ---------------------------------------------------------
# INTERFACE
# ---------------------------------------------------------

for nome, tabela in labs.items():

    tabela = organizar_tabela(tabela)

    if tabela is None:
        continue

    st.subheader(nome)

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )

    st.divider()