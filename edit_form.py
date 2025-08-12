import pandas as pd
import streamlit as st

def render_edit_form(df: pd.DataFrame, file_path: str, cols: list[str]):
    st.divider()
    st.subheader("✏️ Edytuj istniejący rekord")

    binary_cols = {
        'Anoplocephala perfoliata',
        'Oxyuris equi',
        'Parascaris equorum',
        'Strongyloides spp'
    }

    # Formularz wyszukiwania rekordu
    with st.form("search_edit_form"):
        search_id = st.text_input("Podaj **nr zamówienia** rekordu do edycji", key="edit_search")
        search_btn = st.form_submit_button("🔍 Szukaj rekordu")

    if not search_btn or not search_id.strip():
        return df, False

    # Szukamy w DataFrame
    mask = df[' nr zamówienia'].astype(str) == search_id.strip()
    if not mask.any():
        st.error(f"❌ Nie znaleziono rekordu o nr zamówienia: {search_id}")
        return df, False

    # Bierzemy pierwszy pasujący rekord
    idx = df[mask].index[0]
    record = df.loc[idx, :]

    # Formularz edycji
    with st.form("edit_row_form", clear_on_submit=False):
        updated_values = {}

        for c in cols:
            if c in binary_cols:
                updated_values[c] = st.radio(
                    c, options=["0", "1"],
                    index=0 if str(record[c]) == "0" else 1,
                    horizontal=True, key=f"edit_{c}"
                )
            else:
                updated_values[c] = st.text_input(
                    c, value=str(record[c]), key=f"edit_{c}"
                )

        save_btn = st.form_submit_button("💾 Zapisz zmiany", type="primary", use_container_width=True)

    if save_btn:
        for c in cols:
            df.at[idx, c] = updated_values[c]

        try:
            df.to_excel(file_path, index=False)
            st.success("✅ Zmiany zapisano do pliku.")
            st.dataframe(df.loc[[idx]], use_container_width=True)
            return df, True
        except Exception as e:
            st.error(f"❌ Nie udało się zapisać: {e}")
            return df, False

    return df, False