import streamlit as st
import random

st.set_page_config(page_title="끝말잇기", layout="centered")
st.title("📝 끝말잇기 (AI vs 유저)")

# --- 단어 사전 (작은 예시) ---
WORDS = ["사과", "과자", "자동차", "학교", "고양이", "이불", "불고기", "기차", "차표", "표범", "범죄", "죄책감"]

# --- 상태 초기화 ---
if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(WORDS)
    st.session_state.used_words = [st.session_state.current_word]
    st.session_state.game_over = False

def get_next_word(last_char):
    candidates = [w for w in WORDS if w.startswith(last_char) and w not in st.session_state.used_words]
    return random.choice(candidates) if candidates else None

# --- 현재 단어 표시 ---
st.subheader(f"AI 단어: **{st.session_state.current_word}**")
user_input = st.text_input("당신의 단어 입력")

if st.button("제출") and not st.session_state.game_over:
    if user_input not in WORDS:
        st.error("❌ 모르는 단어입니다.")
    elif user_input in st.session_state.used_words:
        st.error("🔁 이미 사용한 단어예요!")
    elif not user_input.startswith(st.session_state.current_word[-1]):
        st.error(f"❌ '{st.session_state.current_word[-1]}'로 시작해야 해요!")
    else:
        st.session_state.used_words.append(user_input)
        next_word = get_next_word(user_input[-1])
        if next_word:
            st.session_state.current_word = next_word
            st.session_state.used_words.append(next_word)
            st.info(f"AI: {next_word}")
        else:
            st.success("🎉 축하합니다! AI가 더 이상 단어를 못 찾았어요.")
            st.session_state.game_over = True

# --- 리셋 ---
if st.button("🔁 다시 시작"):
    st.session_state.current_word = random.choice(WORDS)
    st.session_state.used_words = [st.session_state.current_word]
    st.session_state.game_over = False
    st.rerun()
