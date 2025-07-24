import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", layout="centered")
st.title("✌️✊✋ 가위바위보 게임")

# --- 상태 초기화 ---
if "score_user" not in st.session_state:
    st.session_state.score_user = 0
    st.session_state.score_computer = 0
    st.session_state.round = 0

# --- 선택지 및 결과 판정 함수 ---
choices = {
    "가위": "✌️",
    "바위": "✊",
    "보": "✋"
}

def get_result(user, computer):
    if user == computer:
        return "무승부"
    elif (user == "가위" and computer == "보") or \
         (user == "바위" and computer == "가위") or \
         (user == "보" and computer == "바위"):
        return "승리"
    else:
        return "패배"

# --- 사용자 선택 ---
st.subheader("무엇을 내시겠어요?")
user_choice = st.radio("당신의 선택:", list(choices.keys()), horizontal=True)

# --- 제출 버튼 ---
if st.button("대결"):
    computer_choice = random.choice(list(choices.keys()))
    result = get_result(user_choice, computer_choice)
    st.session_state.round += 1

    # --- 점수 계산 ---
    if result == "승리":
        st.session_state.score_user += 1
    elif result == "패배":
        st.session_state.score_computer += 1

    # --- 결과 출력 ---
    st.markdown(f"### 🧑당신: {choices[user_choice]} ({user_choice})")
    st.markdown(f"### 💻컴퓨터: {choices[computer_choice]} ({computer_choice})")
    
    if result == "승리":
        st.success("🎉당신이 이겼어요")
    elif result == "패배":
        st.error("💥컴퓨터가 이겼어요")
    else:
        st.info("😐무승부입니다!")

# --- 점수판 ---
st.markdown("---")
st.subheader("📊점수판")
st.write(f"👤당신: {st.session_state.score_user}점")
st.write(f"💻컴퓨터: {st.session_state.score_computer}점")
st.write(f"🌀라운드: {st.session_state.round}")

# --- 초기화 버튼 ---
if st.button("🔁 점수 초기화"):
    st.session_state.score_user = 0
    st.session_state.score_computer = 0
    st.session_state.round = 0
    st.rerun()  # ✅ 여기로 수정!

