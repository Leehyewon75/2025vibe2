import streamlit as st
import numpy as np
import random
import copy

st.set_page_config(page_title="스도쿠 게임", layout="centered")
st.title("🧩 스도쿠 퍼즐")

# --- 유효성 검사 및 퍼즐 생성 ---
def is_valid(board, row, col, num):
    if num in board[row]: return False
    if num in board[:, col]: return False
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    if num in board[sr:sr+3, sc:sc+3]: return False
    return True

def solve(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board): return True
                        board[i][j] = 0
                return False
    return True

def generate_sudoku(clues=35):
    board = np.zeros((9, 9), dtype=int)
    solve(board)
    full = copy.deepcopy(board)
    count = 81 - clues
    while count > 0:
        r, c = random.randint(0,8), random.randint(0,8)
        if board[r][c] != 0:
            board[r][c] = 0
            count -= 1
    return board, full

# --- 상태 초기화 ---
if "sudoku" not in st.session_state:
    puzzle, solution = generate_sudoku(clues=35)
    st.session_state.sudoku = puzzle
    st.session_state.solution = solution
    st.session_state.user_input = [[
        "" if puzzle[i][j] == 0 else str(puzzle[i][j])
        for j in range(9)
    ] for i in range(9)]
    st.session_state.checked = False

# --- 새 퍼즐 버튼 ---
if st.button("🔁 새 퍼즐 생성"):
    puzzle, solution = generate_sudoku(clues=35)
    st.session_state.sudoku = puzzle
    st.session_state.solution = solution
    st.session_state.user_input = [[
        "" if puzzle[i][j] == 0 else str(puzzle[i][j])
        for j in range(9)
    ] for i in range(9)]
    st.session_state.checked = False
    st.rerun()

# --- 스도쿠 보드 표시 함수 ---
def render_board():
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            key = f"cell_{i}_{j}"
            is_given = st.session_state.sudoku[i][j] != 0
            value = st.session_state.user_input[i][j]

            # 테두리 스타일: 3x3 블록 기준으로 굵게 표시
            border_style = "border: 1px solid #ccc;"
            if i % 3 == 0 and i != 0:
                border_style += "border-top: 3px solid gray;"
            if j % 3 == 0 and j != 0:
                border_style += "border-left: 3px solid gray;"

            cell_style = f"""
                text-align:center;
                padding:10px;
                background-color:#eee;
                border-radius:4px;
                height: 42px;
                line-height: 22px;
                font-size: 18px;
                {border_style}
            """

            if is_given:
                cols[j].markdown(f"<div style='{cell_style}'>{value}</div>", unsafe_allow_html=True)
            else:
                user_input = cols[j].text_input(
                    "", value, max_chars=1, key=key, label_visibility="collapsed"
                )
                if user_input in "123456789" or user_input == "":
                    st.session_state.user_input[i][j] = user_input

render_board()

# --- 정답 확인 ---
if st.button("✅ 정답 확인"):
    st.session_state.checked = True
    incorrect = False
    for i in range(9):
        for j in range(9):
            if st.session_state.sudoku[i][j] == 0:
                val = st.session_state.user_input[i][j]
                if val != str(st.session_state.solution[i][j]):
                    incorrect = True
    if incorrect:
        st.error("❌ 틀린 곳이 있어요. 다시 시도해보세요!")
    else:
        st.success("🎉 정답입니다!")

# --- 정답 확인 후 틀린 칸 표시 ---
if st.session_state.checked:
    st.subheader("🔎 오답 위치 표시")
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            correct = str(st.session_state.solution[i][j])
            user_val = st.session_state.user_input[i][j]
            is_given = st.session_state.sudoku[i][j] != 0

            border_style = "border: 1px solid #ccc;"
            if i % 3 == 0 and i != 0:
                border_style += "border-top: 3px solid gray;"
            if j % 3 == 0 and j != 0:
                border_style += "border-left: 3px solid gray;"

            style = f"""
                text-align:center;
                padding:10px;
                border-radius:4px;
                height: 42px;
                line-height: 22px;
                font-size: 18px;
                {border_style}
            """

            if is_given:
                cols[j].markdown(
                    f"<div style='background-color:#eee; {style}'>{st.session_state.sudoku[i][j]}</div>",
                    unsafe_allow_html=True)
            else:
                if user_val == "":
                    cols[j].markdown(f"<div style='color:red; {style}'>⬜</div>", unsafe_allow_html=True)
                elif user_val != correct:
                    cols[j].markdown(f"<div style='color:red; {style}'>❌</div>", unsafe_allow_html=True)
                else:
                    cols[j].markdown(f"<div style='color:green; {style}'>✔️</div>", unsafe_allow_html=True)
