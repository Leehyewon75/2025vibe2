import streamlit as st
import random

st.set_page_config(page_title="초성 퀴즈", layout="centered")
st.title("🔠 단어 초성 퀴즈 with 점수 + 힌트")

# --- 퀴즈 데이터: 초성 → (정답, 힌트) ---
QUIZ = {
    "ㅅㄱ": ("사과", "과일 🍎"),
    "ㅂㄹ": ("바나나", "과일 🍌"),
    "ㄱㅂ": ("공부", "학생이 해야 할 것 📚"),
    "ㅎㄱ": ("한국", "우리나라 🇰🇷"),
    "ㅇㄷ": ("운동", "몸을 움직이는 활동 🏃‍♂️"),
    "ㅊㅁ": ("참외", "노란색 과일 🍈"),
    "ㄱㄱ": ("고구마", "군고구마의 주인공 🍠"),
    "ㅈㅂ": ("지방", "서울 외 지역 또는 체지방"),
    "ㅅㅌ": ("스타", "연예인 ⭐"),
    "ㅈㅅ": ("점심", "밥 먹는 시간 🕛")
}

# --- 상태 초기화 ---
if "quiz_key" not in st.session_state:
    st.session_state.quiz_key = random.choice(list(QUIZ.keys()))
    st.session_state.correct = False
    st.session_state.score = 0

# --- 현재 퀴즈 가져오기 ---
quiz = st.session_state.quiz_key
answer, hint = QUIZ[quiz]

# --- 퀴즈 UI ---
st.subheader(f"초성: **{quiz}**")
st.caption(f"힌트: {hint}")
user_input = st.text_input("초성에 맞는 단어를 입력하세요").strip()

# --- 제출 ---
if st.button("제출"):
    if user_input == answer:
        st.success("🎉 정답입니다!")
        st.session_state.correct = True
        st.session_state.score += 1
    else:
        st.error("❌ 오답입니다. 다시 시도해보세요!")
        st.session_state.correct = False

# --- 점수 표시 ---
st.markdown("---")
st.markdown(f"📊 현재 점수: **{st.session_state.score}점**")

# --- 다음 문제 버튼 ---
if st.button("🔁 다음 문제"):
    st.session_state.quiz_key = random.choice(list(QUIZ.keys()))
    st.session_state.correct = False
    st.rerun()
