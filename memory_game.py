import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="미로 탈출 게임", layout="centered")
st.title("🧩 미로 탈출 게임")

# --- 미로 생성 ---
def generate_maze(size=10, wall_prob=0.2):
    maze = np.full((size, size), "⬜")
    for i in range(size):
        for j in range(size):
            if random.random() < wall_prob:
                maze[i][j] = "⬛"

    maze[0][0] = "🟥"  # 시작
    maze[size-1][size-1] = "🟩"  # 도착
    return maze

# --- 초기화 ---
if "maze" not in st.session_state:
    st.session_state.maze = generate_maze()
    st.session_state.pos = [0, 0]
    st.session_state.size = 10
    st.session_state.won = False

maze = st.session_state.maze
x, y = st.session_state.pos
size = st.session_state.size

# --- 승리 여부 확인 ---
if st.session_state.maze[x][y] == "🟩":
    st.session_state.won = True

# --- 미로 UI 표시 ---
def render_maze():
    display = ""
    for i in range(size):
        for j in range(size):
            if [i, j] == st.session_state.pos:
                display += "🟥"
            elif maze[i][j] == "🟩":
                display += "🟩"
            else:
                display += maze[i][j]
        display += "<br>"
    st.markdown(display, unsafe_allow_html=True)

render_maze()

# --- 이동 함수 ---
def move(dx, dy):
    if st.session_state.won:
        return
    nx = st.session_state.pos[0] + dx
    ny = st.session_state.pos[1] + dy
    if 0 <= nx < size and 0 <= ny < size:
        if maze[nx][ny] != "⬛":
            st.session_state.pos = [nx, ny]

# --- 방향 버튼 ---
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️ 위"):
        move(-1, 0)
with col1:
    if st.button("⬅️ 왼쪽"):
        move(0, -1)
with col3:
    if st.button("➡️ 오른쪽"):
        move(0, 1)
with col2:
    if st.button("⬇️ 아래"):
        move(1, 0)

# --- 승리 메시지 ---
if st.session_state.won:
    st.success("🎉 탈출 성공! 도착지에 도달했어요.")

# --- 새 게임 버튼 ---
if st.button("🔁 새 미로 시작"):
    st.session_state.maze = generate_maze()
    st.session_state.pos = [0, 0]
    st.session_state.won = False
