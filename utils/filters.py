# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:39:20 2026

@author: Henery Garção
"""

import streamlit as st

def filtro_texto(df):

    busca = st.text_input("Buscar")

    if busca:
        df = df[
            df.astype(str)
            .apply(lambda x: x.str.contains(busca, case=False))
            .any(axis=1)
        ]

    return df


def filtro_coluna(df, coluna):

    if coluna in df.columns:

        valores = ["Todos"] + list(df[coluna].dropna().unique())

        escolha = st.selectbox(coluna, valores)

        if escolha != "Todos":
            df = df[df[coluna] == escolha]

    return df