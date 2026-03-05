# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:40:10 2026

@author: Henery Garção
"""

import streamlit as st

st.set_page_config(
    page_title="Sistema de Rotinas Acadêmicas",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Sistema de Rotinas Acadêmicas - Profa Dr. Vanessa Ricas Biancardi")

st.markdown("""
Este sistema permite visualizar:

- disciplinas
- horários
- provas
- aulas
- práticas

Use o menu lateral para navegar.
""")

st.info("Plataforma de acompanhamento para alunos e professor.")