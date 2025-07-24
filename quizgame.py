import streamlit as st
import random

# 문제 데이터 (더 추가 가능!)
QUIZZES = [
    {"letters": ['ㅅ', 'ㅏ', 'ㅘ', 'ㄱ'], "answer": "사과", "hint": "과일"},
    {"letters": ['ㅋ', 'ㅓ', 'ㅁ', 'ㅠ', 'ㅍ', 'ㅓ', 'ㅌ'], "answer": "컴퓨터", "hint": "전자기기"},
    {"letters": ['ㅇ', 'ㅛ', 'ㅇ', 'ㄱ', 'ㅘ'], "answer": "용과", "hint": "과일"},
    {"letters": ['ㅂ', 'ㄱ', 'ㅗ', 'ㅅ', 'ㅜ', 'ㅇ', 'ㅇ', 'ㅏ'], "answer": "복숭아", "hint": "과일"},
    {"letters": ['ㅁ', 'ㄹ', 'ㅜ'], "answer": "물", "hint": "마실것"},
    {"letters": ['ㅅ', 'ㄷ', 'ㅜ', 'ㅏ', 'ㄹ'], "answer": "수달", "hint": "동물"},
    {"letters": ['ㅂ', 'ㅕ', 'ㅝ', 'ㄴ', 'ㅇ', 'ㅇ'], "answer": "병원", "hint": "장소"},
    {"letters": ['ㅋ', 'ㅣ', 'ㅟ', 'ㅇ'], "answer": "키위", "hint": "과일"},
    {"letters": ['ㅍ', 'ㄷ', 'ㅗ', 'ㅗ'], "answer": "포도", "hint": "과일"},
    {"letters": ['ㅂ', 'ㄴ', 'ㄴ', 'ㅏ', 'ㅏ', 'ㅏ'], "answer": "바나나", "hint": "과일"},
    {"letters": ['ㅂ', 'ㄹ', 'ㅏ'], "answer": "발", "hint": "신체부위"},
    {"letters": ['ㅎ', 'ㄱ', 'ㄱ', 'ㅏ', 'ㅛ'], "answer": "학교", "hint": "장소"},
    {"letters": ['ㅇ', 'ㅇ', 'ㅑ'], "answer": "양", "hint": "동물"}
    {"letters": ['ㄱ', 'ㄹ', 'ㅣ', 'ㅣ', 'ㄴ'], "answer": "기린", "hint": "동물"},
    {"letters": ['ㄱ', 'ㅇ', 'ㅇ', 'ㅏ', 'ㅏ', 'ㅈ', 'ㅣ'], "answer": "강아지", "hint": "동물"},
    {"letters": ['ㅁ', 'ㅣ', 'ㅓ', 'ㅇ', 'ㅔ', 'ㅅ', 'ㅋ'], "answer": "미어켓", "hint": "동물"},
    {"letters": ['ㅁ', 'ㄹ', 'ㅏ'], "answer": "말", "hint": "동물"},
    {"letters": ['ㄴ', 'ㄱ', 'ㅡ', 'ㄷ', 'ㅐ'], "answer": "늑대", "hint": "동물"},
    {"letters": ['ㅎ', 'ㅁ', 'ㅐ', 'ㅡ', 'ㅅ', 'ㅓ', 'ㅌ'], "answer": "햄스터", "hint": "동물"}
    {"letters": ['ㅌ', 'ㅗ', 'ㅣ', 'ㄲ'], "answer": "토끼", "hint": "동물"},
    {"letters": ['ㅎ', 'ㅐ', 'ㅏ', 'ㅍ', 'ㅣ', 'ㄹ'], "answer": "해파리", "hint": "동물"}
{"letters": ['ㄸ', 'ㄱ', 'ㅏ', 'ㄹ', 'ㅣ'], "answer": "딸기", "hint": "과일"}
]

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.quiz = random.choice(QUIZZES)
    st.session_state.result = None

st.title("🧠 단어 조합 게임")
st.markdown("주어진 글자들을 조합해서 단어를 만들어 보세요!")

quiz = st.session_state.quiz
letters = quiz["letters"]
answer = quiz["answer"]
hint = quiz["hint"]

# 문제 표시
st.subheader("🧩 글자: " + " , ".join(letters))
st.caption(f"💡 힌트: {hint}")

# 입력창
user_input = st.text_input("당신의 단어는?")

# 제출 버튼
if st.button("제출"):
    if user_input.strip() == answer:
        st.success("정답입니다! 🎉")
        st.session_state.score += 1
        st.session_state.result = "correct"
    else:
        st.error(f"틀렸어요! ❌ 정답은 **{answer}** 입니다.")
        st.session_state.result = "wrong"

# 다음 문제
if st.session_state.result:
    if st.button("🔁 다음 문제"):
        st.session_state.quiz = random.choice(QUIZZES)
        st.session_state.result = None
        st.rerun()

# 점수
st.markdown("---")
st.metric(label="누적 점수", value=f"{st.session_state.score} 점")
