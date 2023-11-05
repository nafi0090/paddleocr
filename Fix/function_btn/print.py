import io
import xlsxwriter
import pandas as pd
import streamlit as st

def print(table_df):
    st.markdown('### Unduh Tabel dalam Format Excel')
    # Buat objek BytesIO untuk menyimpan file Excel
    excel_buffer = io.BytesIO()
    # Tulis DataFrame ke dalam objek BytesIO sebagai file Excel
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter', mode='xlsx', options={'remove_timezone': True}) as writer:
        table_df.to_excel(writer, sheet_name='Sheet1', index=False)
    # Unduh data Excel
    excel_buffer.seek(0)
    st.download_button(
        label="Unduh Data dalam Format Excel",
        data=excel_buffer,
        file_name='data BTN.xlsx',  # Nama file yang akan diunduh
        key='excel-download'
    )

    