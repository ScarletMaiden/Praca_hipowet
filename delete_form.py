import pandas as pd
import streamlit as st

def render_delete_form(df: pd.DataFrame, file_path: str):
    st.sidebar.divider()
    st.sidebar.subheader("🗑️ Usuń rekord")

    order_id = st.sidebar.text_input("Podaj nr badania do usunięcia", key="delete_id")
    delete_btn = st.sidebar.button("Usuń rekord", type="primary")

    if delete_btn:
        if not order_id.strip():
            st.sidebar.error("❌ Podaj nr badania.")
            return df, False

        mask = df[' nr zamówienia'].astype(str) == order_id.strip()
        if not mask.any():
            st.sidebar.error(f"❌ Nie znaleziono rekordu o nr badania: {order_id}")
            return df, False


        df_new = df[~mask]

        try:
            df_new.to_excel(file_path, index=False)
            st.sidebar.success("✅ Rekord usunięto.")
            st.success(f"Usunięto rekord o nr badania: {order_id}")
            return df_new, True
        except Exception as e:
            st.sidebar.error(f"❌ Nie udało się zapisać: {e}")
            return df, False


    return df, False
