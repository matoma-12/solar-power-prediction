import streamlit as st
import requests
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os


st.write("📂 Files:")
st.write(os.listdir())

st.write(
    "📦 solar_model.pkl size:",
    os.path.getsize("solar_model.pkl")
)


model = joblib.load("solar_model.pkl")

# 제목
st.title("☀️ Solar Power Prediction System")

st.write(
    "Weather data based AI prediction system for Yeongheung Solar Power Plant"
)


st.subheader("🌤️ Weather Input")


# 날씨 입력
temperature = st.number_input(
    "Temperature (°C)",
    value=25.0
)

wind = st.number_input(
    "Wind Speed (m/s)",
    value=2.0
)

humidity = st.number_input(
    "Humidity (%)",
    value=70
)

# ==========================
# KIER 실시간 일사량 API
# ==========================

import urllib.parse


SERVICE_KEY = "207879c80838329e9010dc7b2f4556f75109de42fd77342f45ad0c34ff1ea5ab"


def get_solar():

    now = datetime.now()

    date = now.strftime("%Y%m%d")
    time = now.strftime("%H00")

    url = (
        "https://apis.data.go.kr/B551184/SrQtyService/getSrQtyStdgInfo"
    )


    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "type": "json",
        "date": date,
        "time": time,
        "stdgCd": "2811010100"
    }


    response = requests.get(
        url,
        params=params
    )


    data = response.json()


    try:
        item = data["response"]["body"]["items"]["item"][0]

        solar = float(
            item["srQty"]
        )

        return solar

   except Exception as e:
    st.write("API 응답 오류:", e)
    st.write("받은 데이터:")
    st.write(data)
    return 0.0


solar = get_solar()


st.metric(
    "☀ Solar Radiation",
    f"{solar} MJ/m²"
)


st.subheader("⚡ Previous Power Information")


previous_power = st.number_input(
    "Previous Power Output (KWh)",
    value=1000.0
)

previous_change = st.number_input(
    "Previous Change Rate",
    value=200.0
)



# 예측 버튼
if st.button("Predict Generation"):


    input_data = pd.DataFrame({

        "기온(°C)": [temperature],
        "풍속(m/s)": [wind],
        "습도(%)": [humidity],
        "일사(MJ/m2)": [radiation],
        "이전 발전량": [previous_power],
        "이전 변화율": [previous_change]

    })


    prediction = model.predict(input_data)


    result = prediction[0]


    st.success(
        f"Predicted Power Generation : {result:.2f} KWh"
    )


    # 결과 그래프

    chart_data = pd.DataFrame({

        "Prediction": [result]

    })


    st.bar_chart(chart_data)



    st.write("Input Data")

    st.dataframe(input_data)
