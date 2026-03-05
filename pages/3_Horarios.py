# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:41:27 2026

@author: Henery Garção
"""

# -*- coding: utf-8 -*-

# import streamlit as st
# import pandas as pd
# from utils.data_loader import carregar_dados

# st.title("📅 Horários")

# dados = carregar_dados()

# if "HORARIOS" not in dados and "HORÁRIOS" not in dados:
#     st.error("A aba HORARIOS não foi encontrada.")
#     st.stop()

# df = dados.get("HORARIOS", dados.get("HORÁRIOS"))

# # df = df.reset_index(drop=True)


# # ---------------------------------------------------------
# # IDENTIFICA OS BLOCOS DA PLANILHA
# # ---------------------------------------------------------

# def separar_blocos(df):

#     blocos = {}

#     bloco_atual = None
#     linhas = []

#     for _, row in df.iterrows():

#         valor = row[0]

#         if isinstance(valor, str):

#             texto = valor.upper()

#             if (
#                 "TÉCNICO" in texto
#                 or "GRADUAÇÃO" in texto
#                 or "ATENDIMENTOS" in texto
#             ):

#                 if bloco_atual and len(linhas) > 0:
#                     blocos[bloco_atual] = pd.DataFrame(linhas)

#                 bloco_atual = valor.strip()
#                 linhas = []
#                 continue

#             if "HORÁRIO PONTO" in texto:
#                 break

#         if bloco_atual:
#             linhas.append(row)

#     if bloco_atual and len(linhas) > 0:
#         blocos[bloco_atual] = pd.DataFrame(linhas)

#     return blocos


# # ---------------------------------------------------------
# # ORGANIZA AS TABELAS
# # ---------------------------------------------------------

# def organizar_tabela(df):

#     df = df.dropna(how="all")

#     if len(df) < 2:
#         return None

#     # primeira linha vira cabeçalho
#     header = df.iloc[0]

#     df = df[1:]

#     df.columns = [
#         "HORÁRIO",
#         "SEGUNDA",
#         "TERÇA",
#         "QUARTA",
#         "QUINTA",
#         "SEXTA"
#     ]

#     df = df.reset_index(drop=True)

#     return df


# # ---------------------------------------------------------
# # PROCESSA OS BLOCOS
# # ---------------------------------------------------------

# blocos = separar_blocos(df)

# if len(blocos) == 0:
#     st.warning("Nenhum horário encontrado na planilha.")
#     st.warning(df.head(40))
#     st.stop()


# # ---------------------------------------------------------
# # INTERFACE STREAMLIT
# # ---------------------------------------------------------

# for nome, tabela in blocos.items():

#     tabela = organizar_tabela(tabela)

#     if tabela is None:
#         continue

#     st.subheader(nome)

#     busca = st.text_input(
#         f"Buscar em {nome}",
#         key=nome
#     )

#     if busca:

#         mask = tabela.astype(str).apply(
#             lambda col: col.str.contains(busca, case=False, na=False)
#         ).any(axis=1)

#         tabela = tabela[mask]

#     st.dataframe(
#         tabela,
#         use_container_width=True
#     )

#     st.divider()


import streamlit as st
import pandas as pd
from utils.data_loader import carregar_dados

st.title("📅 Horários")

dados = carregar_dados()

if "HORARIOS" not in dados and "HORÁRIOS" not in dados:
    st.error("A aba HORARIOS não foi encontrada.")
    st.stop()

df = dados.get("HORARIOS", dados.get("HORÁRIOS"))


# ---------------------------------------------------------
# IDENTIFICA OS BLOCOS DA PLANILHA
# ---------------------------------------------------------

def separar_blocos(df):

    blocos = {}

    bloco_atual = None
    linhas = []

    for _, row in df.iterrows():

        valor = row[0]

        if isinstance(valor, str):

            texto = valor.upper()

            if (
                "TÉCNICO" in texto
                or "GRADUAÇÃO" in texto
                or "ATENDIMENTOS" in texto
            ):

                if bloco_atual and len(linhas) > 0:
                    blocos[bloco_atual] = pd.DataFrame(linhas)

                bloco_atual = valor.strip()
                linhas = []
                continue

            if "HORÁRIO PONTO" in texto:
                break

        if bloco_atual:
            linhas.append(row)

    if bloco_atual and len(linhas) > 0:
        blocos[bloco_atual] = pd.DataFrame(linhas)

    return blocos


# ---------------------------------------------------------
# ORGANIZA AS TABELAS
# ---------------------------------------------------------

def organizar_tabela(df):

    df = df.dropna(how="all")

    if len(df) < 2:
        return None

    df = df[1:]

    df.columns = [
        "HORÁRIO",
        "SEGUNDA",
        "TERÇA",
        "QUARTA",
        "QUINTA",
        "SEXTA"
    ]

    df = df.reset_index(drop=True)

    # troca NaN por vazio
    df = df.fillna("")

    return df


# ---------------------------------------------------------
# PROCESSA OS BLOCOS
# ---------------------------------------------------------

blocos = separar_blocos(df)

if len(blocos) == 0:
    st.warning("Nenhum horário encontrado na planilha.")
    st.write(df.head(40))
    st.stop()


# ---------------------------------------------------------
# INTERFACE STREAMLIT
# ---------------------------------------------------------

for nome, tabela in blocos.items():

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