import streamlit as st
import random

st.set_page_config(page_title="이모지 수학 퍼즐", layout="centered")
st.title("🎲 난이도 선택 가능한 이모지 수학 퍼즐")

# --- 이모지 목록 ---
EMOJIS = ["🍎", "🍌", "🍇", "🍉", "🍓", "🥝", "🍊", "🍍", "🍒"]

# --- 난이도에 따른 숫자 범위 설정 ---
DIFFICULTY_RANGES = {
    "쉬움": (1, 5),
    "보통": (1, 9),
    "어려움": (1, 15)
}

# --- 난이도 선택 ---
difficulty = st.radio("난이도를 선택하세요:", ["쉬움", "보통", "어려움"], horizontal=True)

# --- 퍼즐 생성 함수 ---
def create_puzzle(difficulty_level):
    chosen = random.sample(EMOJIS, 3)
    low, high = DIFFICULTY_RANGES[difficulty_level]
    a, b, c = random.sample(range(low, high + 1), 3)
    puzzle = {
        chosen[0]: a,
        chosen[1]: b,
        chosen[2]: c
    }

    eq1 = f"{chosen[0]} + {chosen[0]} + {chosen[0]} = {a * 3}"
    eq2 = f"{chosen[0]} + {chosen[1]} + {chosen[1]} = {a + b * 2}"
    eq3 = f"{chosen[1]} - {chosen[2]} = {b - c}"
    question = f"{chosen[2]} = ?"

    return {
        "emojis": chosen,
        "values": puzzle,
        "eqs": [eq1, eq2, eq3],
        "question": question
    }

# --- 상태 초기화 ---
if "puzzle" not in st.session_state or st.session_state.get("last_difficulty") != difficulty:
    st.session_state.puzzle = create_puzzle(difficulty)
    st.session_state.answered = False
    st.session_state.last_difficulty = difficulty

data = st.session_state.puzzle
emoji_vals = data["values"]
e1, e2, e3 = data["emojis"]

# --- 수식 표시 ---
st.markdown("### 수식을 보고 이모지 값을 추리해보세요!")
for i, eq in enumerate(data["eqs"], start=1):
    st.markdown(f"**{i}️⃣** {eq}")
st.markdown("---")
st.markdown(f"**❓ 문제: {data['question']}**")

# --- 사용자 입력 받기 ---
answer = st.number_input(f"{e3} 값은 얼마일까요?", step=1, format="%d")

# --- 제출 버튼 ---
if st.button("제출"):
    if int(answer) == emoji_vals[e3]:
        st.success("🎉 정답입니다! 잘했어요.")
    else:
        st.error("❌ 오답입니다. 다시 시도해보세요!")
    st.session_state.answered = True

# --- 새 퍼즐 버튼 ---
if st.button("🔁 새 퍼즐 생성"):
    st.session_state.puzzle = create_puzzle(difficulty)
    st.session_state.answered = False
    st.rerun()
