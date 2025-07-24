import streamlit as st
import random

st.set_page_config(page_title="이모지 퀴즈 게임", layout="centered")
st.title("🤔 이모지 수수께끼 게임")

# --- 문제 데이터 ---
QUIZ = [
    {"emoji": "🔥 + 🍜", "answer": "불닭", "keyword": "라면", "explanation": "매운 라면의 대표주자!"},
    {"emoji": "🐶 + 🍚", "answer": "개밥", "keyword": "반려동물", "explanation": "강아지가 먹는 밥이에요."},
    {"emoji": "🍯 + 🍞", "answer": "꿀빵", "keyword": "간식", "explanation": "달콤한 간식이죠!"},
    {"emoji": "📚 + 🚌", "answer": "통학", "keyword": "학교", "explanation": "학교 갈 때 타는 버스!"},
    {"emoji": "🎃 + 👻", "answer": "할로윈", "keyword": "명절", "explanation": "10월의 유령 파티~"},
    {"emoji": "🚗 + 🏫", "answer": "학원차", "keyword": "교육", "explanation": "학원에서 타고 다니는 차량!"},
    {"emoji": "🧊 + 🧋", "answer": "얼죽아", "keyword": "음료", "explanation": "'얼어 죽어도 아이스 아메리카노'의 줄임말!"},
    {"emoji": "💻 + 🎧", "answer": "재택근무", "keyword": "직장", "explanation": "집에서 일하는 걸 뭐라고 하죠?"},
]

# --- 상태 저장 ---
if "current" not in st.session_state:
    st.session_state.current = random.choice(QUIZ)
    st.session_state.score = 0
    st.session_state.show_result = False
    st.session_state.user_answer = ""

# --- 문제 표시 ---
quiz = st.session_state.current
st.markdown(f"### 이모지: {quiz['emoji']}")
st.caption(f"💡 키워드 힌트: *{quiz['keyword']}*")

# --- 사용자 입력 ---
user_input = st.text_input("정답을 입력하세요!", value=st.session_state.user_answer)

if st.button("제출") or st.session_state.show_result:
    st.session_state.user_answer = user_input
    if not st.session_state.show_result:
        if user_input.strip() == quiz["answer"]:
            st.success("🎉 정답입니다!")
            st.session_state.score += 1
        else:
            st.error("❌ 오답이에요!")
        st.info(f"📘 해설: **{quiz['explanation']}**")
        st.markdown(f"✅ 정답은 **{quiz['answer']}** 였습니다.")
        st.session_state.show_result = True

# --- 다음 문제 ---
if st.session_state.show_result:
    if st.button("🔁 다음 문제"):
        st.session_state.current = random.choice(QUIZ)
        st.session_state.show_result = False
        st.session_state.user_answer = ""
        st.rerun()

# --- 점수 표시 ---
st.markdown("---")
st.metric(label="현재 점수", value=f"{st.session_state.score} 점")
