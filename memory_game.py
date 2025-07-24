import streamlit as st
import random
import time

# --- 설정 ---
LEVELS = {
    "초급 (4x4)": (4, 4),
    "중급 (5x4)": (5, 4),
    "고급 (6x6)": (6, 6),
}

EMOJIS = ["🍎", "🍌", "🍒", "🍇", "🍓", "🍍", "🥝", "🥑",
          "🍉", "🍑", "🥥", "🍋", "🍈", "🌽", "🍅", "🍆",
          "🥕", "🥔"]

# --- 최고 기록 저장 함수 ---
@st.cache_data(show_spinner=False)
def get_high_scores():
    return {}

def update_high_score(level, attempts, elapsed):
    scores = get_high_scores()
    best = scores.get(level, {"attempts": float("inf"), "time": float("inf")})

    updated = False
    if attempts < best["attempts"] or (attempts == best["attempts"] and elapsed < best["time"]):
        best["attempts"] = attempts
        best["time"] = elapsed
        scores[level] = best
        st.cache_data.clear()
        st.cache_data(show_spinner=False)(lambda: scores)()
        updated = True

    return updated

# --- 상태 초기화 ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'flipped' not in st.session_state:
    st.session_state.flipped = []
if 'matched' not in st.session_state:
    st.session_state.matched = []
if 'cards' not in st.session_state:
    st.session_state.cards = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'level' not in st.session_state:
    st.session_state.level = "초급 (4x4)"

# --- 타이머 ---
def get_elapsed_time():
    if st.session_state.start_time:
        return int(time.time() - st.session_state.start_time)
    return 0

# --- 카드 초기 생성 ---
def init_game(level):
    rows, cols = LEVELS[level]
    total_cards = rows * cols
    assert total_cards % 2 == 0

    pairs = EMOJIS[:total_cards // 2] * 2
    random.shuffle(pairs)

    st.session_state.cards = pairs
    st.session_state.flipped = []
    st.session_state.matched = []
    st.session_state.attempts = 0
    st.session_state.start_time = time.time()
    st.session_state.game_started = True

# --- 카드 뒤집기 ---
def flip_card(index):
    if index in st.session_state.flipped or index in st.session_state.matched:
        return

    st.session_state.flipped.append(index)

    if len(st.session_state.flipped) == 2:
        i1, i2 = st.session_state.flipped
        st.session_state.attempts += 1
        if st.session_state.cards[i1] == st.session_state.cards[i2]:
            st.session_state.matched.extend([i1, i2])
        time.sleep(0.5)
        st.session_state.flipped = []

# --- UI ---
st.title("🃏 기억력 카드 맞추기 게임")

# 최고 기록 표시
high_scores = get_high_scores()
if st.session_state.level in high_scores:
    hs = high_scores[st.session_state.level]
    st.info(f"🏆 최고 기록 - {st.session_state.level}: {hs['attempts']}회 시도, {hs['time']}초")

# 레벨 선택 & 시작
if not st.session_state.game_started:
    level = st.selectbox("난이도 선택", list(LEVELS.keys()), index=list(LEVELS.keys()).index(st.session_state.level))
    if st.button("게임 시작"):
        st.session_state.level = level
        init_game(level)
else:
    rows, cols = LEVELS[st.session_state.level]
    cards = st.session_state.cards

    st.write(f"🧠 시도 횟수: {st.session_state.attempts}회")
    st.write(f"⏱️ 경과 시간: {get_elapsed_time()}초")

    for r in range(rows):
        cols_ui = st.columns(cols)
        for c in range(cols):
            idx = r * cols + c
            label = "❓"
            if idx in st.session_state.matched or idx in st.session_state.flipped:
                label = cards[idx]
            if cols_ui[c].button(label, key=f"card_{idx}"):
                flip_card(idx)

    # 승리 시
    if len(st.session_state.matched) == len(cards):
        elapsed = get_elapsed_time()
        st.success(f"🎉 축하합니다! 모든 카드를 맞췄어요.")
        st.write(f"총 시도: {st.session_state.attempts}회")
        st.write(f"총 소요 시간: {elapsed}초")

        updated = update_high_score(st.session_state.level, st.session_state.attempts, elapsed)
        if updated:
            st.balloons()
            st.success("📈 새로운 최고 기록입니다!")

        if st.button("다시 시작"):
            st.session_state.game_started = False
