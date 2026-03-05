# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:41:43 2026

@author: Henery Garção
"""

import streamlit as st
from utils.data_loader import get_provas
from utils.filters import filtro_texto

st.title("📝 Provas")

df = get_provas()

df = filtro_texto(df)

st.dataframe(df, use_container_width=True)