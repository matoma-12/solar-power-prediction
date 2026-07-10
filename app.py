import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt


# 모델 불러오기
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

radiation = st.number_input(
    "Solar Radiation (MJ/m²)",
    value=15.0
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
