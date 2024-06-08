# 환경 설정
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from collections import Counter
import folium
from streamlit_folium import st_folium

# 파일 불러오기
text_file = pd.read_csv("streamlit_cluster(04.24).csv")
latlon = text_file.groupby('Store').first()[['Y', 'X']]
Review_text = text_file[['Store','Review_text','sentiment','cluster']]

# 페이지를 session_state에 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# 사용자 함수 정의
def button_click(page):
    st.session_state.page = page

# 메인 홈페이지
def home_page():

    # 배경사진
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:url("https://i.imgur.com/wtY58mv.png");
        background-attachment:fixed;
        background-size:cover
        
    }}
    </style>
    """,
    unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Hi Bread!</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 25px; font-family: Noto Sans CJK KR, sans-serif;'>네게 맛집만 보여줄게, 좋아하는 🥖키워드를 눌러볼래?</h1>", unsafe_allow_html=True)

    # HTML을 사용하여 버튼의 스타일을 조정
    st.markdown("""
        <style>
            /* 버튼의 너비를 190px로 지정 */
            .stButton>button {
                width: 200px;
                height: 60px;
            }
        </style>
    """, unsafe_allow_html=True)

    left, mid, right = st.columns([0.1,2,0.1])

    with mid:
        b1, b2, b3 = st.columns(3)
        b1.button('내가 찾던 빵맛집👍', type="primary", on_click=button_click, args=("cluster_0",))
        b2.button('멋진 뷰와 분위기', type="primary", on_click=button_click, args=("cluster_1",))
        b3.button('기가 막히는 음료', type="primary", on_click=button_click, args=("cluster_2",))
        
        b4, b5, b6 = st.columns(3)
        b4.button('넓고 쾌적한 매장', type="primary", on_click=button_click, args=("cluster_3",))
        b5.button('아름다운 인테리어', type="primary", on_click=button_click, args=("cluster_4",))
        b6.button('그외 빵집도 궁금해', type="primary", on_click=button_click, args=("cluster_5",))

# 누가 궁금해? 페이지
def breadmap():

    # 배경사진
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:url("https://i.imgur.com/wtY58mv.png");
        background-attachment:fixed;
        background-size:cover
        
    }}
    </style>
    """,
    unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Click me!</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 25px; font-family: Noto Sans CJK KR, sans-serif;'>네게 리뷰를 모아서 보여줄게, 어떤 🥖맛집이 궁금해?</h1>", unsafe_allow_html=True)

    # HTML을 사용하여 버튼의 스타일을 조정
    st.markdown("""
        <style>
            /* 버튼의 너비를 350px로 지정 */
            .stButton>button {
                width: 200px;
                height: 60px;
            }
        </style>
    """, unsafe_allow_html=True)

    left, mid, right = st.columns([0.1,2,0.1])
    
    flag = True
    while flag:
        if st.session_state.cluster == 'cluster_0':
            random_store = text_file[text_file['cluster'] == 1]['Store'].sample(n=9)
            store_name(random_store)
        elif st.session_state.cluster == 'cluster_1':
            random_store = text_file[text_file['cluster'] == 2]['Store'].sample(n=9)
            store_name(random_store)
        elif st.session_state.cluster == 'cluster_2':
            random_store = text_file[text_file['cluster'] == 3]['Store'].sample(n=9)
            store_name(random_store)
        elif st.session_state.cluster == 'cluster_3':
            random_store = text_file[text_file['cluster'] == 4]['Store'].sample(n=9)
            store_name(random_store)
        elif st.session_state.cluster == 'cluster_4':
            random_store = text_file[text_file['cluster'] == 5]['Store'].sample(n=9)
            store_name(random_store)
        elif st.session_state.cluster == 'cluster_5':
            random_store = text_file[text_file['cluster'] == 0]['Store'].sample(n=9)
            store_name(random_store)
        
        # 중복 가게 제거
        counter = Counter(random_store)
        counter_list = list(counter.values())
        if max(counter_list) == 1:
            flag=False
    
    with mid:
        b1, b2, b3 = st.columns(3)
        b1.button(f'{random_store.iloc[0]}',type="primary", on_click=button_click, args=("store_0",), key='store_0_button')
        b2.button(f'{random_store.iloc[1]}',type="primary", on_click=button_click, args=("store_1",), key='store_1_button')
        b3.button(f'{random_store.iloc[2]}',type="primary", on_click=button_click, args=("store_2",), key='store_2_button')
    
        b4, b5, b6 = st.columns(3)
        b4.button(f'{random_store.iloc[3]}',type="primary", on_click=button_click, args=("store_3",), key='store_3_button')
        b5.button(f'{random_store.iloc[4]}',type="primary", on_click=button_click, args=("store_4",), key='store_4_button')
        b6.button(f'{random_store.iloc[5]}',type="primary", on_click=button_click, args=("store_5",), key='store_5_button')

        b7, b8, b9 = st.columns(3)
        b7.button(f'{random_store.iloc[6]}',type="primary", on_click=button_click, args=("store_6",), key='store_6_button')
        b8.button(f'{random_store.iloc[7]}',type="primary", on_click=button_click, args=("store_7",), key='store_7_button')
        b9.button(f'{random_store.iloc[8]}',type="primary", on_click=button_click, args=("store_8",), key='store_8_button')

        c1, c2, c3 = st.columns(3)
        c1.button("처음으로 돌아가기", on_click=button_click, args=("home",))

# 친구 소개하기 페이지
def friend():

    # 배경사진
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:url("https://i.imgur.com/wtY58mv.png");
        background-attachment:fixed;
        background-size:cover
        
    }}
    </style>
    """,
    unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Introduce myself!</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # 가게 소개
        cond5 = (text_file['cluster']==st.session_state.num)
        information = text_file[cond5].groupby('Store').first()[['Review_score','Address','행정동명','cluster_labeling']]
        cond1 = (information.index == f'{st.session_state.name}')

        st.write("🍰Here's Bakery information")
        df_int = pd.DataFrame({
            '이름': [f'🥖 {st.session_state.name}'],
            '평점': f'⭐ {information[cond1].iloc[0].values[0]}',
            '특성': [information[cond1].iloc[0].values[3]],
            '행정동': [information[cond1].iloc[0].values[2]],
            '주소': [information[cond1].iloc[0].values[1]]
        })
        st.dataframe(df_int, use_container_width=True)

        cond = (latlon.index == f'{st.session_state.name}')

        st.write("🍩Here's Bakery Location")

        map_data = pd.DataFrame({
            'lat': [latlon[cond].iloc[0].values[0]],
            'lon': [latlon[cond].iloc[0].values[1]]
        })
        lat = latlon[cond].iloc[0].values[0]
        lon = latlon[cond].iloc[0].values[1]
        latlon_save(lat, lon)

        # Folium 지도 생성
        map = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup=st.session_state.name).add_to(map)
        st_folium(map, width=800, height=300)

        st.markdown("""
            <style>
                /* 버튼의 너비를 350px로 지정 */
                .stButton>button {
                    width: 345px;
                }
            </style>
        """, unsafe_allow_html=True)

        st.button("다른 친구 알아보기", type="primary", on_click=button_click, args=("breadmap",))

    with col2:

        # 불호 리뷰
        cond2 = (Review_text['Store'] == f'{st.session_state.name}')
        cond3 = (Review_text['sentiment'] == 1)
        cond4 = (Review_text['sentiment'] == 0)
        cond6 = (Review_text['cluster'] == st.session_state.num)

        st.write("👎Here's Bakery Negative reviews (부정리뷰)")
        st.dataframe(pd.DataFrame({
            '리뷰 더블클릭': Review_text[cond2&cond4&cond6]['Review_text']
        }).reset_index(drop=True), use_container_width=True, height=212)

        # 극호 리뷰
        st.write("👍Here's Bakery Positive reviews (긍정리뷰)")
        try:
            st.dataframe(pd.DataFrame({
                '리뷰 더블클릭': Review_text[cond2&cond3&cond6]['Review_text']
            }).reset_index(drop=True), use_container_width=True, height=300)
        except:
            st.write(pd.DataFrame({
                '리뷰 더블클릭': ['불호 리뷰가 없어요!']
            }).reset_index(drop=True))
        
        st.button("1 Km 이내 비슷한 빵집을 알려줄게", on_click=button_click, args=("new_friend1",))
        st.button("3 Km 이내 비슷한 빵집을 알려줄게", on_click=button_click, args=("new_friend3",))

# 1km 이내의 새로운 친구보기
def new_friend1():

    # 배경사진
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:url("https://i.imgur.com/wtY58mv.png");
        background-attachment:fixed;
        background-size:cover
        
    }}
    </style>
    """,
    unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Introduce my friend!</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 25px; font-family: Noto Sans CJK KR, sans-serif;'>네게 1km이내 친구들을 보여줄게, 어떤 🥖맛집이 궁금해?</h1>", unsafe_allow_html=True)

    # HTML을 사용하여 버튼의 스타일을 조정
    st.markdown("""
        <style>
            /* 버튼의 너비를 350px로 지정 */
            .stButton>button {
                width: 200px;
                height: 60px;
            }
        </style>
    """, unsafe_allow_html=True)

    import math

    def haversine(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        R = 6371.0

        distance = R * c

        return distance
    
    latlon2 = text_file[text_file['cluster']==st.session_state.num].groupby('Store').first()[['Y', 'X']]
    dis1 = []
    dis3 = []
    for i in range(len(latlon2)):
        lat1, lon1 = (37.5604164, 126.9662337)
        lat2, lon2 = tuple(latlon2.iloc[i])
        distance = haversine(lat1, lon1, lat2, lon2)
        if distance <= 1:
            dis1.append(latlon2.index[i])
        if distance <= 3: # elif말고 if로 중복허용
            dis3.append(latlon2.index[i])

    # 리스트의 순서를 무작위로 섞기
    import random
    random.shuffle(dis1)
    new_friend_name1(dis1)

    left, mid, right = st.columns([0.1,2,0.1])
    
    with mid:
        for i in range(0, 9, 3):  # 3개씩 끊어서 반복
            # 현재 줄에 대한 컬럼을 생성
            cols = st.columns(3)
            # 현재 줄에 버튼을 최대 3개까지 생성
            for j in range(3): # 0,1,2
                if i + j < len(dis1):  # dis1 리스트의 범위 내에 있을 때만 버튼 생성
                    cols[j].button(dis1[i+j], type="primary", on_click=button_click, args=(f"new1store_{i+j}",), key=f'new1store_{i+j}_button')

# 3km 이내의 새로운 친구보기
def new_friend3():

    # 배경사진
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:url("https://i.imgur.com/wtY58mv.png");
        background-attachment:fixed;
        background-size:cover
        
    }}
    </style>
    """,
    unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Introduce my friend!</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 25px; font-family: Noto Sans CJK KR, sans-serif;'>네게 3km이내 친구들을 보여줄게, 어떤 🥖맛집이 궁금해?</h1>", unsafe_allow_html=True)

    # HTML을 사용하여 버튼의 스타일을 조정
    st.markdown("""
        <style>
            /* 버튼의 너비를 350px로 지정 */
            .stButton>button {
                width: 200px;
                height: 60px;
            }
        </style>
    """, unsafe_allow_html=True)

    import math

    def haversine(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        R = 6371.0

        distance = R * c

        return distance
    
    latlon2 = text_file[text_file['cluster']==st.session_state.num].groupby('Store').first()[['Y', 'X']]
    dis1 = []
    dis3 = []
    for i in range(len(latlon2)):
        lat1, lon1 = (37.5604164, 126.9662337)
        lat2, lon2 = tuple(latlon2.iloc[i])
        distance = haversine(lat1, lon1, lat2, lon2)
        if distance <= 1:
            dis1.append(latlon2.index[i])
        if distance <= 3: # elif말고 if로 중복허용
            dis3.append(latlon2.index[i])

    # 리스트의 순서를 무작위로 섞기
    import random
    random.shuffle(dis3)
    new_friend_name3(dis3)

    left, mid, right = st.columns([0.1,2,0.1])
    
    with mid:
        for i in range(0, 9, 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dis3):
                    cols[j].button(dis3[i+j], type="primary", on_click=button_click, args=(f"new3store_{i+j}",), key=f'new3store_{i+j}_button')

# 페이지 렌더링
if st.session_state.page == "home":
    print(st.session_state.page)
    home_page()
elif st.session_state.page == "breadmap":
    print(st.session_state.page)
    st.session_state.page = st.session_state.cluster
    breadmap()
elif st.session_state.page == "new_friend1":
    print(st.session_state.page)
    new_friend1()
elif st.session_state.page == "new_friend3":
    print(st.session_state.page)
    new_friend3()
for e in range(6):
    if st.session_state.page == f"cluster_{e}":
        print(st.session_state.page)
        cluster_name(st.session_state.page)
        breadmap()
for e in range(9):
    if st.session_state.page == f"store_{e}":
        print(st.session_state.page)
        st.session_state.name = st.session_state.store_name[e]
        friend()
for e in range(9):
    if st.session_state.page == f"new1store_{e}":
        print(st.session_state.page)
        st.session_state.name = st.session_state.name_list1[e]
        friend()
for e in range(9):
    if st.session_state.page == f"new3store_{e}":
        print(st.session_state.page)
        st.session_state.name = st.session_state.name_list3[e]
        friend()