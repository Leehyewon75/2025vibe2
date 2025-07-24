import streamlit as st
import random

st.set_page_config(page_title="랜덤 이모지 수학 퍼즐", layout="centered")
st.title("🎲 랜덤 이모지 수학 퍼즐")

# --- 이모지 리스트 ---
EMOJIS = ["🍎", "🍌", "🍇", "🍉", "🍓", "🥝", "🍊", "🍍", "🍒"]

# --- 퍼즐 초기화 ---
def create_puzzle():
    chosen = random.sample(EMOJIS, 3)
    a, b, c = random.sample(range(1, 10), 3)
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

# --- 상태 저장 ---
if "puzzle" not in st.session_state:
    st.session_state.puzzle = create_puzzle()
    st.session_state.answered = False

data = st.session_state.puzzle
emoji_vals = data["values"]
e1, e2, e3 = data["emojis"]

# --- 수식 출력 ---
st.markdown("### 🧠 수식을 보고 이모지 값을 추리해보세요!")
for idx, eq in enumerate(data["eqs"], start=1):
    st.markdown(f"**{idx}️⃣** {eq}")
st.markdown("---")
st.markdown(f"**❓ 문제: {data['question']}**")

# --- 정답 입력 ---
answer = st.number_input(f"{e3} 값은 얼마일까요?", step=1, format="%d")

# --- 제출 버튼 ---
if st.button("제출"):
    if int(answer) == emoji_vals[e3]:
        st.success("🎉 정답입니다! 잘했어요.")
    else:
        st.error(f"❌ 오답이에요. 다시 시도해보세요!")
    st.session_state.answered = True

# --- 새 문제 버튼 ---
if st.button("🔁 새 퍼즐 생성"):
    st.session_state.puzzle = create_puzzle()
    st.session_state.answered = False
    st.rerun()
