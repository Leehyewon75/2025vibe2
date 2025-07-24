import streamlit as st
import random

st.set_page_config(page_title="이모지 맞추기 퀴즈", layout="centered")
st.title("🐾 이모지 맞추기 게임")

# --- 문제 데이터 ---
QUIZ = [
    {"emoji": "🔥 + 🐔", "answer": "불닭", "keyword": "라면, 2글자"},
    {"emoji": "🐶 + 🍚", "answer": "개밥", "keyword": "반려동물"},
    {"emoji": "🍯 + 🍞", "answer": "꿀빵", "keyword": "간식"},
    {"emoji": "🧀 + 🎂", "answer": "치즈케이크", "keyword": "음식, 5글자"},
    {"emoji": "🎃 + 👻", "answer": "할로윈", "keyword": "명절"},
    {"emoji": "🚗 + 🏫", "answer": "학원차", "keyword": "교육"},
    {"emoji": "🧊 + 🧋", "answer": "얼죽아", "keyword": "음료"},
    {"emoji": "❄️ + 🏰", "answer": "겨울왕국", "keyword": "영화, 4글자"},
    {"emoji": "🐰 + 🦊", "answer": "주토피아", "keyword": "영화, 4글자"},
    {"emoji": "🖤 + 🩷", "answer": "블랙핑", "keyword": "아이돌, 4글자"}
]

# --- 상태 저장 ---
if "current" not in st.session_state:
    st.session_state.current = random.choice(QUIZ)
    st.session_state.score = 0
    st.session_state.show_result = False
    st.session_state.user_answer = ""

quiz = st.session_state.current
st.markdown(f"### 이모지: {quiz['emoji']}")
st.caption(f"💡 키워드 힌트: *{quiz['keyword']}*")

# --- 입력 받기 ---
user_input = st.text_input("정답을 입력하세요!", value=st.session_state.user_answer)

# --- 제출 ---
if st.button("제출") or st.session_state.show_result:
    st.session_state.user_answer = user_input
    if not st.session_state.show_result:
        if user_input.strip() == quiz["answer"]:
            st.success("🎉 정답입니다!")
            st.session_state.score += 1
        else:
            st.error("❌ 오답이에요!")
            st.info(f"📌 정답은 **{quiz['answer']}** 입니다.")
        st.session_state.show_result = True

# --- 다음 문제 버튼 ---
if st.session_state.show_result:
    if st.button("🔁 다음 문제"):
        st.session_state.current = random.choice(QUIZ)
        st.session_state.show_result = False
        st.session_state.user_answer = ""
        st.rerun()

# --- 점수 표시 ---
st.markdown("---")
st.metric(label="현재 점수", value=f"{st.session_state.score} 점")
