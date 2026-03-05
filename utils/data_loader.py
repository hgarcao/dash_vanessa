# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:38:22 2026

@author: Henery Garção
"""

import pandas as pd
import streamlit as st

ARQUIVO = "data/rotinas.xlsx"


def limpar_colunas(df):
    """Garante nomes de colunas válidos e únicos."""

    cols = []
    usados = {}

    for i, c in enumerate(df.columns):

        if pd.isna(c):
            c = f"COL_{i}"

        c = str(c)

        if c in usados:
            usados[c] += 1
            c = f"{c}_{usados[c]}"
        else:
            usados[c] = 0

        cols.append(c)

    df.columns = cols

    return df


def limpar_tabela(df):

    if df.empty:
        return df

    # primeira linha vira cabeçalho
    df.columns = df.iloc[0]

    df = df.drop(0)

    df = df.dropna(how="all")

    df = limpar_colunas(df)

    df = df.reset_index(drop=True)

    return df


# @st.cache_data
# def carregar_dados():

#     xls = pd.ExcelFile(ARQUIVO)

#     dados = {}

#     for aba in xls.sheet_names:

#         # HORÁRIOS precisa header=None
#         if aba.upper() == "HORÁRIOS":

#             df = pd.read_excel(
#                 xls,
#                 sheet_name=aba,
#                 header=None
#             )

#             df.columns = [f"COL_{i}" for i in range(len(df.columns))]

#             dados["HORARIOS"] = df

#         else:

#             df = pd.read_excel(
#                 xls,
#                 sheet_name=aba
#             )

#             dados[aba.upper()] = df

#     return dados

@st.cache_data
def carregar_dados():

    xls = pd.ExcelFile(ARQUIVO)

    dados = {}

    for aba in xls.sheet_names:

        nome = aba.upper()

        # abas com múltiplas tabelas
        if nome in ["HORÁRIOS", "HORARIOS", "PRÁTICAS", "PRATICAS"]:

            df = pd.read_excel(
                xls,
                sheet_name=aba,
                header=None
            )

            # garante colunas consistentes
            df.columns = [f"COL_{i}" for i in range(len(df.columns))]

            dados[nome] = df

        else:

            df = pd.read_excel(
                xls,
                sheet_name=aba
            )

            dados[nome] = df

    return dados

def get_aba(nome):

    dados = carregar_dados()

    nome = nome.upper()

    if nome not in dados:
        return pd.DataFrame()

    return dados[nome]


def get_disciplina():
    return get_aba("DISCIPLINAS")


def get_horarios():
    return get_aba("HORÁRIOS")


def get_provas():
    return get_aba("PROVAS")


def get_aulas():
    return get_aba("AULAS")


def get_praticas():
    return get_aba("PRÁTICAS")

def extrair_tabelas_horarios():

    df = pd.read_excel(
        ARQUIVO,
        sheet_name="HORÁRIOS",
        header=None
    )

    tabelas = {}
    titulo_atual = None
    buffer = []

    for _, row in df.iterrows():

        primeira = row.iloc[0]

        if isinstance(primeira, str):

            nome = primeira.strip().upper()

            if (
                "TÉCNICO" in nome
                or "GRADUAÇÃO" in nome
                or "ATENDIMENTOS" in nome
            ):

                if titulo_atual and buffer:
                    tabelas[titulo_atual] = pd.DataFrame(buffer)

                titulo_atual = nome
                buffer = []

                continue

            if "PONTO" in nome:
                titulo_atual = None
                buffer = []
                continue

        if titulo_atual:
            buffer.append(row.values)

    if titulo_atual and buffer:
        tabelas[titulo_atual] = pd.DataFrame(buffer)

    # limpar cada tabela
    for nome in tabelas:

        df = tabelas[nome]

        df.columns = df.iloc[0]
        df = df.drop(0)

        df = df.dropna(how="all")

        df = df.reset_index(drop=True)

        tabelas[nome] = df

    return tabelas


def get_horarios():

    return extrair_tabelas_horarios()
