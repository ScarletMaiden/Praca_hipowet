import os
import pandas as pd
import streamlit as st
from add_form import render_add_form
from edit_form import render_edit_form
from delete_form import render_delete_form

FILE_PATH = "praca.xlsx"
COLS = [
    ' nr zamówienia', 'nr badania', 'imię konia',
    'Anoplocephala perfoliata', 'Oxyuris equi', 'Parascaris equorum',
    'Strongyloides spp', 'Kod-pocztowy ', 'Miasto '
]

st.set_page_config(page_title="Zamówienia", page_icon="📦", layout="wide")
st.title("📦 Podgląd i dodawanie zamówień")


def load_df(path: str, cols: list[str]) -> pd.DataFrame:
    if not os.path.exists(path):
        df0 = pd.DataFrame({c: pd.Series(dtype="string") for c in cols})
        df0.to_excel(path, index=False)
        return df0
    df0 = pd.read_excel(path, dtype=str)

    for c in cols:
        if c not in df0.columns:
            df0[c] = pd.Series(dtype="string")
    return df0[cols]

df = load_df(FILE_PATH, COLS)


with st.sidebar:
    st.header("🔎 Wyszukiwanie")
    q = st.text_input("Numer zamówienia (część lub całość)", placeholder="np. 12345")
    search = st.button("Szukaj")


st.subheader("📄 Wyniki wyszukiwania" if (search and q.strip()) else "📄 Wszystkie dane")
if search and q.strip():
    mask = df[' nr zamówienia'].astype(str).str.contains(q.strip(), case=False, na=False)
    res = df.loc[mask]
    if res.empty:
        st.info("Brak wyników.")
        st.dataframe(df, use_container_width=True, height=420)
    else:
        st.success(f"Znaleziono {len(res)} rekord(y).")
        st.dataframe(res, use_container_width=True, height=420)
else:
    st.dataframe(df, use_container_width=True, height=420)


df, saved = render_add_form(df, FILE_PATH, COLS)
df, _ = render_edit_form(df, FILE_PATH, COLS)
df, _ = render_delete_form(df, FILE_PATH)
if saved:

    st.rerun()