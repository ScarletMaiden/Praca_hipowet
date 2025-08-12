import pandas as pd
import streamlit as st

def render_add_form(df: pd.DataFrame, file_path: str, cols: list[str]):
    st.divider()
    st.subheader("➕ Dodaj nowy rekord")

    # Kolumny binarne (0/1)
    binary_cols = {
        'Anoplocephala perfoliata',
        'Oxyuris equi',
        'Parascaris equorum',
        'Strongyloides spp'
    }

    with st.form("add_row_form", clear_on_submit=True):
        values = {}

        for c in cols:
            if c in binary_cols:
                values[c] = st.radio(
                    c, options=["0", "1"], index=0, horizontal=True, key=f"in_{c}"
                )
            else:
                values[c] = st.text_input(c, value="", key=f"in_{c}")

        submitted = st.form_submit_button("Enter ↵", type="primary", use_container_width=True)

    if not submitted:
        return df, False

    nr = (values.get(' nr zamówienia') or "").strip()
    if nr == "":
        st.error("Pole **' nr zamówienia'** jest wymagane.")
        return df, False


    new_row = {c: (values.get(c) or "").strip() for c in cols}

    df_new = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    try:
        df_new.to_excel(file_path, index=False)
        st.success("✅ Dodano nowy wiersz i zapisano do pliku.")
        st.dataframe(df_new.tail(10), use_container_width=True, height=260)
        st.caption(f"Aktualna liczba wierszy: {len(df_new)}")
        return df_new, True
    except Exception as e:
        st.error(f"❌ Nie udało się zapisać: {e}")
        return df, False
