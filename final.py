import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import streamlit as st
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 도입 페이지 제목
st.markdown("""
<div style="text-align: center; font-size: 36px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;">
    🚲 공공자전거(따릉이) 활성화 정책<br>
    우리가 제안해보자! 🌱
</div>
""", unsafe_allow_html=True)

# 페이지 설명
st.markdown("""
<div style="background-color: #e6f7ff; padding: 15px; border-radius: 10px; border: 2px solid #b3e0ff; text-align: center;">
    서울시 공공자전거 <b>따릉이</b>는 누구나 이용가능한 자전거 무인 대여 시스템이에요.<br>
    환경도 지키고 건강도 챙기는 따릉이를 더 많이 이용하면 좋겠죠? 🚴‍♂🌿
</div>
""", unsafe_allow_html=True)
# 홈 페이지
page = st.sidebar.selectbox("메뉴 선택", ["홈", "따릉이 데이터", "지도 데이터", "환경 데이터"])
if page == "홈":
    st.image("따릉이소개.jpeg", caption="서울자전거 개요", use_container_width=True)
    st.image("따릉이 실제 사진.jpeg", caption="서울 시내 따릉이 대여소 모습", use_container_width=True)
    st.image("공공자전거.jpg", caption="따릉이 일러스트", use_container_width=True)
    
# 페이지 안내
st.markdown("""
<div style="background-color: #f0f9eb; padding: 15px; border-radius: 10px; border: 2px solid #c3e6cb; margin-top: 20px; text-align: center;">
    📊 <b>사이드바에서 원하는 시각화 페이지를 선택하세요!</b><br><br>
    🚴‍♀️ <b>따릉이 데이터</b><br>
    🗺 <b>지도 데이터</b><br>
    📈 <b>환경 데이터</b>
</div>
""", unsafe_allow_html=True)

# 정리 페이지로 이동하는 버튼 생성
if st.sidebar.button("📝 정리 페이지로 이동"):
    page = "정리 페이지"



# 홈 페이지에서 다른 페이지의 시각화 숨기기
if page == "홈":
    st.stop()


# 따릉이 데이터 페이지
if page == "따릉이 데이터":
    st.title("📊 따릉이 이용 현황 분석")
    
    # 성별 이용건수 분석
    st.subheader("1. 성별 따릉이 이용건수")
    st.image("성별 따릉이 이용건수.png", caption="성별 이용건수 분석", use_container_width=True)

    # 연령대별 이용건수 분석
    st.subheader("2. 연령대별 따릉이 이용건수")
    st.image("연령대별 따릉이 이용건수.png", caption="연령대별 이용건수 분석", use_container_width=True)

    # 시간대별 이용건수 분석
    st.subheader("3. 시간대별 따릉이 이용건수")
    st.image("시간대별 따릉이 이용건수.png", caption="시간대별 이용건수 분석", use_container_width=True)

    # 요일별 이용건수 분석
    st.subheader("4. 요일별 따릉이 이용건수")
    st.image("요일별 따릉이 이용건수.png", caption="요일별 이용건수 분석", use_container_width=True)

# 지도 데이터 페이지
if page == "지도 데이터":
    st.markdown("""
    <div style="text-align: center; font-size: 36px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;">
    🗺 서울시 00구별<br>
    따릉이 위치와 인구밀도
    </div>
    """, unsafe_allow_html=True)

    
    # 로컬 파일 경로 설정
    population_data_path = "서울시 인구밀도.xlsx"
    bike_data_path = "공공자전거 대여소 정보(24.6월 기준).xlsx"
    geojson_path = "서울특별시 지역구.geojson"

    # 파일 존재 여부 확인 함수
    def check_file_path(path, description):
        if not os.path.exists(path):
            st.error(f"{description} 파일을 찾을 수 없습니다: {path}")
            st.stop()

    check_file_path(population_data_path, "서울시 인구밀도 데이터")
    check_file_path(bike_data_path, "공공자전거 대여소 데이터")
    check_file_path(geojson_path, "서울특별시 지역구 GeoJSON")

    # 데이터 불러오기
    population_data = pd.read_excel(population_data_path)
    bike_data = pd.read_excel(bike_data_path, sheet_name='대여소현황')
    geo_data = gpd.read_file(geojson_path)

    # 위도와 경도에서 NaN 값 제거 및 타입 변환
    bike_data = bike_data.dropna(subset=['위도', '경도'])
    bike_data['위도'] = pd.to_numeric(bike_data['위도'], errors='coerce')
    bike_data['경도'] = pd.to_numeric(bike_data['경도'], errors='coerce')
    bike_data = bike_data.dropna(subset=['위도', '경도'])

    # GeoJSON과 인구밀도 데이터 병합
    geo_data = geo_data.merge(population_data, left_on="sggnm", right_on="자치구")

    # 지도 생성
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # 인구밀도 단계 구분도 (Choropleth)
    folium.Choropleth(
        geo_data=geo_data,
        data=population_data,
        columns=["자치구", "인구밀도 (명/㎢)"],
        key_on="feature.properties.sggnm",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="서울시 인구밀도 (명/㎢)"
    ).add_to(m)

    # GeoJson으로 지역구 경계선 강조 및 이름 표시
    folium.GeoJson(
        geo_data,
        name="서울시 지역구 경계",
        style_function=lambda x: {
            "fillOpacity": 0,
            "color": "black",
            "weight": 1
        },
        tooltip=folium.GeoJsonTooltip(fields=["sggnm"], aliases=["지역구"], style="font-weight: bold;")
    ).add_to(m)

    # 따릉이 대여소 위치를 작은 연한 점으로 추가
    for _, row in bike_data.iterrows():
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=1,
            color="#66b3ff",
            fill=True,
            fill_color="#66b3ff",
            fill_opacity=0.2,
        ).add_to(m)

     # Streamlit에 지도 표시
    st_folium(m, width=700, height=500)

    # 지역구별 대여소 개수 및 인구밀도 순위 표시
    st.subheader("지역구별 따릉이 대여소 개수 및 인구밀도 순위")
    district_counts = bike_data['자치구'].value_counts().reset_index()
    district_counts.columns = ["자치구", "대여소 개수"]
    
    # 인구밀도 데이터와 병합
    district_data = district_counts.merge(population_data, on="자치구")
    district_data = district_data.sort_values(by="대여소 개수", ascending=False)
    district_data["인구밀도 순위"] = district_data["인구밀도 (명/㎢)"].rank(ascending=False).astype(int)
    
    st.dataframe(district_data)

    # 지도 설명 추가
    st.markdown("""
    ### 설명
    - **파란 점**: 따릉이 대여소 위치를 나타냅니다.
    - **색상 구분**: 지역구별 인구밀도를 나타냅니다 (단계구분도).
    """)


# 환경 데이터 페이지
if page == "환경 데이터":
    st.markdown("""
    <div style="text-align: center; font-size: 36px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;">
    🌦 강수량, 미세먼지, 기온에 따른<br>
    따릉이 대여건수
    </div>
    """, unsafe_allow_html=True)
  
    
    # 데이터 정의
    data = {
        "월": ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        "평균기온 (℃)": [-1.9, 0.4, 6.5, 12.8, 18.2, 22.5, 25.7, 26.1, 21.5, 15.1, 7.5, 0.1],
        "평균 미세먼지 농도 (㎍/㎥)": [34.8, 38.2, 45.0, 42.3, 35.7, 28.4, 25.1, 22.8, 26.3, 30.7, 33.5, 37.9],
        "평균 강수량 (mm)": [16.8, 25.0, 48.2, 77.3, 102.5, 150.3, 414.4, 326.7, 169.4, 52.1, 53.8, 30.4],
        "따릉이 대여건수": [1570000, 1800000, 3200000, 4000000, 4500000, 5000000, 4800000, 4600000, 4700000, 4900000, 4200000, 3800000]
    }
    
    df = pd.DataFrame(data)
    
    # 따릉이 대여건수를 만 단위로 변환
    df["따릉이 대여건수 (만 건)"] = df["따릉이 대여건수"] / 10000
    
    # 옵션 선택
    selected_option = st.radio("원하는 그래프를 선택하세요:", ["평균 강수량 (mm)", "평균 미세먼지 농도 (㎍/㎥)", "평균기온 (℃)"])
    
    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    # 선택된 옵션에 따른 그래프
    ax1.plot(df["월"], df[selected_option], marker='o', color='b', label=selected_option)
    ax2.plot(df["월"], df["따릉이 대여건수 (만 건)"], marker='o', color='r', linestyle='--', label="따릉이 대여건수 (만 건)")
    
    # 축 레이블
    ax1.set_xlabel("월")
    ax1.set_ylabel(selected_option, color='b')
    ax2.set_ylabel("따릉이 대여건수 (만 건)", color='r')
    
    # 범례
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    # 제목
    plt.title(f"{selected_option} 및 따릉이 대여건수 비교")
    
    # 그래프 표시
    st.pyplot(plt)
    
    # 설명 추가
    st.markdown("""
    ### 설명
    - **파란 선**: 선택된 데이터 (강수량, 미세먼지 농도, 기온)
    - **빨간 점선**: 따릉이 대여건수 (만 건)
    """)
    
# 정리 페이지
if page == "정리 페이지":
    st.markdown("""
    <div style="text-align: center; font-size: 36px; font-weight: bold; color: #34495e; margin-bottom: 20px;">
        📝 정리 페이지
    </div>
    """, unsafe_allow_html=True)
    
    # 1. 선택한 데이터와 자료
    st.subheader("1. 선택한 데이터와 자료")
    selected_data = st.text_area("선택한 데이터와 자료를 입력하세요.")
    
    # 2. 선택한 데이터와 자료를 통해 알 수 있는 점
    st.subheader("2. 선택한 데이터와 자료를 통해 알 수 있는 점")
    insights = st.text_area("데이터를 통해 추론해낸 정보를를 작성하세요.")
    
    # 3. 공공자전거(따릉이) 활성화를 위한 정책 제시
    st.subheader("3. 공공자전거(따릉이) 활성화를 위한 정책 제시")
    policy_suggestion = st.text_area("따릉이 활성화를 위한 정책을 제안하세요.")
    
    # 제출 버튼
    if st.button("제출"):
        st.success("정리 내용이 성공적으로 저장되었습니다!")
