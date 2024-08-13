import streamlit as st
import requests
import pandas as pd

# 사이드바 설정
with st.sidebar:
    notion_token = st.text_input("노션 TOKEN을 입력해주세요.")
    st.markdown("##### 노션 TOKEN 생성 방법 [바로가기](https://www.notion.so/profile/integrations)")
    
    for i in range(4):
        st.markdown("")

    if notion_token:
        database_id = st.text_input("데이터 베이스 ID를 입력해주세요.")
        st.markdown("#### --- 노션 데이터베이스 링크 복사 방법 ---")
        st.markdown("01. 노션에서 맨 오른쪽 위 ... 버튼을 클릭하세요. ")
        st.markdown("02. 연결 탭에서 생성한 API를 연결해주세요. ")
        st.markdown("03. 노션 데이터베이스 링크를 복사합니다. ")
        st.markdown("04. `https://www.notion.so/<데이터 베이스 ID>?v=<무시 가능>` ")
        st.markdown("05. 데이터 베이스 ID를 입력창에 넣어주세요.")
        
# 메인 코드
if notion_token:
    if database_id:
        # 검색 위젯
        search_name = st.text_input("검색할 이름을 입력하세요:")

        # Notion API 요청
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        response = requests.post(url=url, headers=headers)
        data = response.json()

        # 이름을 저장할 리스트 및 ID 리스트
        names = []
        ids = []
        urls = []

        # JSON 데이터를 순회하여 이름과 URL을 추출
        for page in data['results']:
            properties = page.get('properties', {})
            name_property = properties.get('이름', {})
            title_list = name_property.get('title', [])
            page_id = page.get('id', '')
            page_url = f"https://www.notion.so/{page_id.replace('-', '')}"

            if title_list:
                for title in title_list:
                    names.append(title.get('text', {}).get('content', ''))
                    ids.append(page_id)
                    urls.append(page_url)
            else:
                names.append('이름이 없습니다.')
                ids.append(page_id)
                urls.append(page_url)

        # DataFrame으로 변환
        df = pd.DataFrame({
            '이름': names,
            'URL': urls
        })

        # 검색된 이름으로 필터링
        if search_name:
            search_df = df[df['이름'].str.contains(search_name, case=False, na=False)]

            if not search_df.empty:
                st.write("검색된 결과:")
                st.write(search_df)
            else:
                st.write("검색 결과가 없습니다.")
        else:
            st.write("전체 데이터:")
            st.write(df)
    else: 
        st.markdown("노션 데이터베이스 ID를 입력해주세요.")
else:
    st.markdown("노션 TOKEN을 입력해주세요.")
