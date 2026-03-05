# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:40:59 2026

@author: Henery Garção
"""

import streamlit as st
from utils.data_loader import get_disciplina

st.title("📚 Disciplinas")

df = get_disciplina()

if df.empty:
    st.warning("Aba DISCIPLINAS não encontrada.")
    st.stop()

df = df.fillna("")

col1, col2, col3 = st.columns(3)

categoria = col1.selectbox(
    "Categoria",
    ["Todas"] + sorted(df["CATEGORIA"].astype(str).unique())
)

curso = col2.selectbox(
    "Curso",
    ["Todos"] + sorted(df["CURSO"].astype(str).unique())
)

periodo = col3.selectbox(
    "Período",
    ["Todos"] + sorted(df["PERÍODO"].astype(str).unique())
)

if categoria != "Todas":
    df = df[df["CATEGORIA"] == categoria]

if curso != "Todos":
    df = df[df["CURSO"] == curso]

if periodo != "Todos":
    df = df[df["PERÍODO"] == periodo]

st.dataframe(df, use_container_width=True)