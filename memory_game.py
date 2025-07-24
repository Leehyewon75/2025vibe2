import streamlit as st

st.set_page_config(page_title="이모지 수학 퍼즐", layout="centered")
st.title("🍎🍌 이모지 수학 퍼즐")

# --- 퍼즐 정의 ---
PUZZLE = {
    "🍎": 5,
    "🍌": 7,
    "🍇": 4
}

# 수식 구성
eq1 = f"{'🍎'} + {'🍎'} + {'🍎'} = {PUZZLE['🍎'] * 3}"
eq2 = f"{'🍎'} + {'🍌'} + {'🍌'} = {PUZZLE['🍎'] + PUZZLE['🍌'] * 2}"
eq3 = f"{'🍌'} - {'🍇'} = {PUZZLE['🍌'] - PUZZLE['🍇']}"
question = f"{'🍇'} = ?"

# --- UI 표시 ---
st.markdown("### 🧠 수식을 보고 이모지 값을 추리해보세요!")
st.markdown(f"**1️⃣** {eq1}")
st.markdown(f"**2️⃣** {eq2}")
st.markdown(f"**3️⃣** {eq3}")
st.markdown("---")
st.markdown(f"**❓ 문제: {question}**")

# --- 정답 입력 ---
answer = st.number_input("🍇 값은 얼마일까요?", step=1, format="%d")

# --- 정답 확인 ---
if st.button("제출"):
    if int(answer) == PUZZLE["🍇"]:
        st.success("🎉 정답입니다! 잘했어요.")
    else:
        st.error("❌ 오답이에요. 다시 생각해보세요!")

# --- 새 게임 안내 (단일 퍼즐 고정형) ---
st.info("이 버전은 고정된 퍼즐입니다. 원하면 랜덤 퍼즐 버전도 만들어줄게요!")
