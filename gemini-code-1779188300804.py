import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="나만의 동물 아바타 상점", page_icon="🐾", layout="centered")

# --- 1. 전역 데이터베이스 설정 ---
ANIMALS = {
    "일반": [
        '시바견', '말티즈', '푸들', '포메라니안', '웰시코기', '비글', '리트리버', '닥스훈트', '퍼그', '불독',
        '치즈냥', '고등어냥', '턱시도냥', '삼색이', '하얀 고양이', '검은 고양이', '샴', '러시안블루', '페르시안', '스코티시 폴드',
        '햄스터', '다람쥐', '하얀 토끼', '갈색 토끼', '롭이어 토끼', '기니피그', '친칠라', '고슴도치', '하늘다람쥐', '미어캣',
        '병아리', '오리', '닭', '앵무새', '참새', '비둘기', '뵤뵤뱁새', '문조', '카나리아', '아기 부엉이',
        '아기 돼지', '꼬마 양', '젖소', '미니 말', '아기 염소', '알파카', '거위', '나귀', '라마', '쿼카'
    ],
    "희귀": [
        '사막여우', '붉은여우', '레서판다', '자이언트 판다', '아기 호랑이', '아기 사자', '늑대', '수달', '보노보노 해달', '코알라',
        '황제펭귄', '아기 물개', '하프물범', '돌고래', '범고래', '벨루가', '바다거북', '해마', '흰곰', '귀여운 문어',
        '아기 사슴', '순록', '너구리', '스컹크', '카피바라', '나무늘보', '플라밍고', '공작새', '사막 도마뱀', '카멜레온'
    ],
    "전설": [
        '아기 드래곤', '아기 유니콘', '페가수스', '불사조 병아리', '구미호 아기여우', '해태', '그리핀', '크라켄', '켈베로스', '피닉스',
        '황금 시바견', '갤럭시 고양이', '오로라 펭귄', '별빛 토끼', '사이버네틱 햄스터', '초코 퐁듀 베어', '젤리 슬라임 냥', '유령 아기돼지', '무지개 알파카', '달빛 여우'
    ]
}

ITEMS = [
    # 머리 (Head) - 20종
    {"name": '빨간 리본', "cat": '머리'}, {"name": '왕관', "cat": '머리'}, {"name": '신사 중절모', "cat": '머리'}, {"name": '요리사 모자', "cat": '머리'}, {"name": '생일 축하 고깔', "cat": '머리'},
    {"name": '천사 링', "cat": '머리'}, {"name": '악마 뿔', "cat": '머리'}, {"name": '새싹 핀', "cat": '머리'}, {"name": '요정 화관', "cat": '머리'}, {"name": '마녀 모자', "cat": '머리'},
    {"name": '해적 모자', "cat": '머리'}, {"name": '귀도리', "cat": '머리'}, {"name": '군대 철모', "cat": '머리'}, {"name": '야구 모자', "cat": '머리'}, {"name": '탐정 모자', "cat": '머리'},
    {"name": '온천 수건', "cat": '머리'}, {"name": '달걀 프라이 핀', "cat": '머리'}, {"name": '바나나 껍질', "cat": '머리'}, {"name": '상어 모자', "cat": '머리'}, {"name": '인디언 깃털', "cat": '머리'},
    # 얼굴 (Face) - 20종
    {"name": '동글이 안경', "cat": '얼굴'}, {"name": '하트 뿅뿅 안경', "cat": '얼굴'}, {"name": '멋쟁이 선글라스', "cat": '얼굴'}, {"name": '탐정 돋보기', "cat": '얼굴'}, {"name": '해적 안대', "cat": '얼굴'},
    {"name": '연고 반창고', "cat": '얼굴'}, {"name": '볼빨간 홍조', "cat": '얼굴'}, {"name": '콧수염', "cat": '얼굴'}, {"name": '도둑 수염', "cat": '얼굴'}, {"name": '보석 눈물', "cat": '얼굴'},
    {"name": '뱅글뱅글 안경', "cat": '얼굴'}, {"name": '3D 안경', "cat": '얼굴'}, {"name": '장미 입에 물기', "cat": '얼굴'}, {"name": '쪽쪽이', "cat": '얼굴'}, {"name": '버블티 빨대', "cat": '얼굴'},
    {"name": '닌자 복면', "cat": '얼굴'}, {"name": '산타 수염', "cat": '얼굴'}, {"name": '방독면', "cat": '얼굴'}, {"name": '사이버그 안구', "cat": '얼굴'}, {"name": '단안경', "cat": '얼굴'},
    # 의상 (Body) - 20종
    {"name": '미니 탐정 망토', "cat": '의상'}, {"name": '영웅 빨간 망토', "cat": '의상'}, {"name": '임금님 곤룡포', "cat": '의상'}, {"name": '턱시도', "cat": '의상'}, {"name": '웨딩드레스', "cat": '의상'},
    {"name": '알록달록 패딩', "cat": '의상'}, {"name": '멜빵바지', "cat": '의상'}, {"name": '수영복', "cat": '의상'}, {"name": '해리포터 로브', "cat": '의상'}, {"name": '투명 망토', "cat": '의상'},
    {"name": '크리스마스 산타복', "cat": '의상'}, {"name": '꿀벌 옷', "cat": '의상'}, {"name": '공룡 잠옷', "cat": '의상'}, {"name": '죄수복', "cat": '의상'}, {"name": '바나나 슈트', "cat": '의상'},
    {"name": '우주복', "cat": '의상'}, {"name": '세일러복', "cat": '의상'}, {"name": '가죽 자켓', "cat": '의상'}, {"name": '천사 날개', "cat": '의상'}, {"name": '악마 날개', "cat": '의상'},
    # 소품 (Hand) - 20종
    {"name": '마법 지팡이', "cat": '소품'}, {"name": '별빛 요술봉', "cat": '소품'}, {"name": '대파', "cat": '소품'}, {"name": '생선 가시', "cat": '소품'}, {"name": '장난감 칼', "cat": '소품'},
    {"name": '하트 풍선', "cat": '소품'}, {"name": '큼직한 고기', "cat": '소품'}, {"name": '아메리카노', "cat": '소품'}, {"name": '쥐불놀이', "cat": '소품'}, {"name": '황금 주머니', "cat": '소품'},
    {"name": '무지개 우산', "cat": '소품'}, {"name": '족발', "cat": '소품'}, {"name": '도토리 가방', "cat": '소품'}, {"name": '곰돌이 인형', "cat": '소품'}, {"name": '거대 연필', "cat": '소품'},
    {"name": '반짝이는 등불', "cat": '소품'}, {"name": '닌자 표창', "cat": '소품'}, {"name": '일렉 기타', "cat": '소품'}, {"name": '전설의 성검', "cat": '소품'}, {"name": '댕댕이 뼈다귀', "cat": '소품'},
    # 이펙트 (Effect) - 20종
    {"name": '하트 뿅뿅 오라', "cat": '이펙트'}, {"name": '반짝이는 별가루', "cat": '이펙트'}, {"name": '먹구름과 번개', "cat": '이펙트'}, {"name": '낙엽 휘날림', "cat": '이펙트'}, {"name": '벚꽃 엔딩', "cat": '이펙트'},
    {"name": '불타는 투지', "cat": '이펙트'}, {"name": '얼음 장판', "cat": '이펙트'}, {"name": '돈벼락 효과', "cat": '이펙트'}, {"name": '무지개 발자국', "cat": '이펙트'}, {"name": '음표 둥둥', "cat": '이펙트'},
    {"name": '유령 출몰', "cat": '이펙트'}, {"name": '황금빛 오우라', "cat": '이펙트'}, {"name": '사이버 네온 링', "cat": '이펙트'}, {"name": '메트릭스 코드', "cat": '이펙트'}, {"name": '나비 정원', "cat": '이펙트'},
    {"name": '먼지 뽀뽀작', "cat": '이펙트'}, {"name": '시계태엽 환영', "cat": '이펙트'}, {"name": '우주 성운 배경', "cat": '이펙트'}, {"name": '디스코 조명', "cat": '이펙트'}, {"name": '압도적 아우라', "cat": '이펙트'}
]

# --- 2. 세션 상태(State) 초기화 ---
if 'gold' not in st.session_state:
    st.session_state.gold = 1000
if 'animal' not in st.session_state:
    st.session_state.animal = None
if 'rank' not in st.session_state:
    st.session_state.rank = None
if 'slots' not in st.session_state:
    st.session_state.slots = {'머리': '없음', '얼굴': '없음', '의상': '없음', '소품': '없음', '이펙트': '없음'}
if 'log' not in st.session_state:
    st.session_state.log = "✨ 인형 가게에 오신 것을 환영합니다!"

# --- 3. UI 레이아웃 설계 ---
st.title("🐾 귀여운 아바타 인형 가게")
st.caption("나만의 펫을 뽑고 100종의 다양한 소품으로 코디해 보세요!")

# 대시보드 상단 (골드 보유 현황)
st.subheader(f"💰 현재 보유 골드: {st.session_state.gold} G")
st.progress(min(st.session_state.gold / 3000, 1.0)) # 3000G 기준 진행 바 고정

st.divider()

# 메인 디스플레이 영역 (아바타 결과판)
with st.container():
    st.markdown("### 🪞 현재 아바타 상태")
    
    # 등급별 커스텀 스타일 박스 설정
    if st.session_state.animal:
        rank_colors = {"일반": "#757575", "희귀": "#1e88e5", "전설": "#ff1744"}
        color = rank_colors.get(st.session_state.rank, "#333")
        st.markdown(f"#### 🏷️ 등급: <span style='color:{color}; font-weight:bold;'>[{st.session_state.rank}]</span>", unsafe_allow_html=True)
        st.info(f"🐱 **동물 종류**: {st.session_state.animal}")
    else:
        st.warning("🥚 알이 아직 부화하지 않았습니다. 아래 상점에서 부화시켜 주세요!")

    # 장착 슬롯 리스트 배치
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"🧢 **머리**: {st.session_state.slots['머리']}")
        st.write(f"👓 **얼굴**: {st.session_state.slots['얼굴']}")
        st.write(f"👕 **의상**: {st.session_state.slots['의상']}")
    with col2:
        st.write(f"🪄 **소품**: {st.session_state.slots['소품']}")
        st.write(f"✨ **이펙트**: {st.session_state.slots['이펙트']}")

st.divider()

# 액션 및 가챠 상점 영역
st.markdown("### 🛒 상점 골라 가기")
act_col, gacha1_col, gacha2_col = st.columns(3)

with act_col:
    if st.button("💸 알바 뛰기 (+100G)", use_container_width=True):
        st.session_state.gold += 100
        st.session_state.log = "🛒 아르바이트를 성공적으로 마쳐 100G를 획득했습니다!"
        st.rerun()

with gacha1_col:
    if st.button("🥚 알 뽑기 (-100G)", use_container_width=True):
        if st.session_state.gold >= 100:
            st.session_state.gold -= 100
            
            # 50%, 30%, 20% 가중치 무작위 뽑기
            rng = random.randint(0, 99)
            if rng < 50:
                st.session_state.rank = "일반"
                st.session_state.animal = random.choice(ANIMALS["일반"])
            elif rng < 80:
                st.session_state.rank = "희귀"
                st.session_state.animal = random.choice(ANIMALS["희귀"])
            else:
                st.session_state.rank = "전설"
                st.session_state.animal = random.choice(ANIMALS["전설"])
            
            # 새로운 동물이 태어나면 장착 아이템 리셋
            st.session_state.slots = {'머리': '없음', '얼굴': '없음', '의상': '없음', '소품': '없음', '이펙트': '없음'}
            st.session_state.log = f"🎉 쾅! [{st.session_state.rank}] 등급의 '{st.session_state.animal}'이(가) 태어났습니다!"
            st.rerun()
        else:
            st.session_state.log = "❌ 골드가 부족합니다! 알바를 먼저 뛰어주세요."

with gacha2_col:
    if st.button("🎀 템 뽑기 (-50G)", use_container_width=True):
        if not st.session_state.animal:
            st.session_state.log = "⚠️ 장착할 동물이 없습니다. 먼저 동물 알을 뽑아주세요!"
        elif st.session_state.gold >= 50:
            st.session_state.gold -= 50
            
            # 아이템 100종 중 하나 무작위 추첨
            picked_item = random.choice(ITEMS)
            category = picked_item["cat"]
            item_name = picked_item["name"]
            
            # 부위 스토리지 분기 업데이트
            st.session_state.slots[category] = item_name
            st.session_state.log = f"🎁 아이템 획득! {category} 슬롯에 [{item_name}]을(를) 장착했습니다!"
            st.rerun()
        else:
            st.session_state.log = "❌ 골드가 부족합니다! 알바를 먼저 뛰어주세요."

# 하단 최근 행동 로그 메시지창
st.code(f"알림 로그: {st.session_state.log}")