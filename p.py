import streamlit as st
import requests
import pandas as pd

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBUS-JBKLQqTfq2CPXNytxeUfSaTjekeL1K"
DEVICE_LABEL = "hsc345"
VARIABLES = ["mq2", "humidity", "temperature", "lux"]

def get_ubidots_data(variable_label):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{variable_label}/values"
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return None

st.title("📊 Dashboard Sensor ESP32 (Ubidots)")

# Layout 2 kolom
col1, col2 = st.columns(2)

# Loop tiap variabel
for i, var in enumerate(VARIABLES):
    data = get_ubidots_data(var)

    if data:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        # Ambil nilai terbaru
        latest = df.iloc[0]['value']
        timestamp = df.iloc[0]['timestamp']

        # Tampilkan di kolom
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.metric(label=f"{var.upper()} (Latest)", value=round(latest, 2))
            st.line_chart(df[['timestamp', 'value']].set_index('timestamp'))

    else:
        st.error(f"❌ Gagal mengambil data dari variabel: {var}")
