import streamlit as st
import random

st.set_page_config(page_title="초성 퀴즈", layout="centered")
st.title("🔠 단어 초성 퀴즈!")

# --- 초성 데이터셋 ---
QUIZ = {
    "ㅅㄱ": "사과",
    "ㅂㄹ": "바나나",
    "ㄱㅂ": "공부",
    "ㅎㄱ": "한국",
    "ㅇㄷ": "운동",
    "ㅊㅁ": "참외",
    "ㄱㄱ": "고구마",
    "ㅈㅂ": "지방",
    "ㅅㅌ": "스타",
    "ㅈㅅ": "점심"
}

# --- 상태 초기화 ---
if "quiz_key" not in st.session_state:
    st.session_state.quiz_key = random.choice(list(QUIZ.keys()))
    st.session_state.correct = False

quiz = st.session_state.quiz_key
answer = QUIZ[quiz]

st.subheader(f"초성: **{quiz}**")
user = st.text_input("초성에 맞는 단어를 입력하세요").strip()

if st.button("제출"):
    if user == answer:
        st.success("🎉 정답입니다!")
        st.session_state.correct = True
    else:
        st.error("❌ 오답입니다. 다시 시도해보세요!")

if st.session_state.correct:
    if st.button("🔁 다음 문제"):
        st.session_state.quiz_key = random.choice(list(QUIZ.keys()))
        st.session_state.correct = False
        st.rerun()
