import streamlit as st
import random

st.set_page_config(page_title="Wordle 게임", layout="centered")
st.title("🟩 단어 추리 게임 (Wordle 스타일)")

# --- 단어 목록 (원한다면 외부 txt 파일로 분리 가능) ---
WORDS = ["APPLE", "GRAPE", "BRAVE", "PLANT", "CRANE", "SMART", "GLASS", "TRUST", "STORY", "CANDY"]

# --- 상태 초기화 ---
if "target" not in st.session_state:
    st.session_state.target = random.choice(WORDS)
    st.session_state.attempts = []
    st.session_state.game_over = False
    st.session_state.success = False

# --- 입력 ---
if not st.session_state.game_over:
    guess = st.text_input("5글자 영어 단어를 입력하세요", max_chars=5).upper()

    if st.button("제출"):
        if len(guess) != 5 or guess not in WORDS:
            st.warning("유효한 5글자 영어 단어를 입력하세요.")
        else:
            st.session_state.attempts.append(guess)

            if guess == st.session_state.target:
                st.session_state.game_over = True
                st.session_state.success = True
            elif len(st.session_state.attempts) >= 6:
                st.session_state.game_over = True

# --- 힌트 표시 함수 ---
def render_guess_row(guess, target):
    result = []
    for i in range(5):
        if guess[i] == target[i]:
            result.append(f"<span style='background-color:#6aaa64;color:white;padding:8px;border-radius:4px;margin:2px;font-weight:bold;'>{guess[i]}</span>")
        elif guess[i] in target:
            result.append(f"<span style='background-color:#c9b458;color:white;padding:8px;border-radius:4px;margin:2px;font-weight:bold;'>{guess[i]}</span>")
        else:
            result.append(f"<span style='background-color:#787c7e;color:white;padding:8px;border-radius:4px;margin:2px;font-weight:bold;'>{guess[i]}</span>")
    return " ".join(result)

# --- 시도된 단어 표시 ---
st.markdown("### 시도 기록")
for word in st.session_state.attempts:
    st.markdown(render_guess_row(word, st.session_state.target), unsafe_allow_html=True)

# --- 결과 메시지 ---
if st.session_state.game_over:
    if st.session_state.success:
        st.success("🎉 정답입니다!")
    else:
        st.error(f"😢 실패! 정답은 **{st.session_state.target}** 였습니다.")

    if st.button("🔁 다시 시작"):
        st.session_state.clear()
        st.experimental_rerun()
