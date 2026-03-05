# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:40:28 2026

@author: Henery Garção
"""

import streamlit as st
from utils.data_loader import carregar_dados

st.title("📊 Visão Geral")

dados = carregar_dados()

col1, col2, col3 = st.columns(3)

col1.metric("Disciplinas", len(dados.get("DISCIPLINAS", [])))
col2.metric("Aulas", len(dados.get("AULAS", [])))
col3.metric("Provas", len(dados.get("PROVAS", [])))
