import streamlit as st
import pandas as pd
import numpy as np
import requests
import joblib
from datetime import datetime


# ==========================
# 모델 불러오기
# ==========================

@st.cache_resource
def load_model():
    return joblib.load("solar_model.pkl")


model = load_model()
# ==========================
# 제목
# ==========================

st.title("☀ Solar Power Prediction AI")
st.write("Real-time weather data based solar power prediction")


# ==========================
# 실시간 일사량 API
# ==========================

def get_solar():

    now = datetime.now()

    date = now.strftime("%Y%m%d")
    time = now.strftime("%H00")


    url = "https://apis.data.go.kr/B551184/SrQtyService"


    params = {
        "serviceKey": "207879c80838329e9010dc7b2f4556f75109de42fd77342f45ad0c34ff1ea5ab",
        "pageNo": "1",
        "numOfRows": "10",
        "dataType": "JSON",
        "base_date": date,
        "base_time": time
    }


    response = requests.get(
        url,
        params=params
    )


    # API 확인용
   st.write("API status:", response.status_code)


    try:

        data = response.json()

        item = data["response"]["body"]["items"]["item"][0]


        # 아직 실제 변수명 모름
        # API 결과 보고 수정 예정
        solar = float(item["srQty"])

        return solar


except Exception as e:
    st.error(e)
    return 0.0


# ==========================
# 입력값
# ==========================

st.subheader("Weather Input")


temperature = st.number_input(
    "Temperature (°C)",
    value=25.0
)


wind = st.number_input(
    "Wind speed (m/s)",
    value=2.0
)


humidity = st.number_input(
    "Humidity (%)",
    value=60.0
)


previous_power = st.number_input(
    "Previous Power Output (KWh)",
    value=1000.0
)


previous_change = st.number_input(
    "Previous Change Rate",
    value=0.0
)



# ==========================
# API 실행
# ==========================

solar = get_solar()


st.metric(
    "☀ Solar Radiation (MJ/m²)",
    solar
)



# ==========================
# 예측
# ==========================

if st.button("Predict Power Generation"):


    input_data = pd.DataFrame(
        [[
            temperature,
            wind,
            humidity,
            solar,
            previous_power,
            previous_change
        ]],
        columns=[
            "기온(°C)",
            "풍속(m/s)",
            "습도(%)",
            "일사(MJ/m2)",
            "이전 발전량",
            "이전 변화율"
        ]
    )


    prediction = model.predict(
        input_data
    )


    st.success(
        f"Predicted Power Generation: {prediction[0]:.2f} KWh"
    )
