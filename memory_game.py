import streamlit as st
import numpy as np
import random
import copy

st.set_page_config(page_title="HTML 스도쿠", layout="centered")
st.title("🧩 HTML 기반 스도쿠")

# --- 스도쿠 생성 함수 ---
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
    st.session_state.user_input = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.checked = False

# --- 새 퍼즐 버튼 ---
if st.button("🔁 새 퍼즐 생성"):
    puzzle, solution = generate_sudoku(clues=35)
    st.session_state.sudoku = puzzle
    st.session_state.solution = solution
    st.session_state.user_input = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.checked = False
    st.rerun()

# --- 스타일 ---
def get_cell_style(i, j, is_fixed, is_wrong=False):
    style = "width:40px; height:40px; text-align:center; font-size:20px;"
    style += "border:1px solid #999;"
    if i % 3 == 0:
        style += "border-top: 2px solid black;"
    if j % 3 == 0:
        style += "border-left: 2px solid black;"
    if i == 8:
        style += "border-bottom: 2px solid black;"
    if j == 8:
        style += "border-right: 2px solid black;"
    if is_fixed:
        style += "background-color:#eee;"
    elif is_wrong:
        style += "background-color:#ffcccc;"
    elif not is_fixed:
        style += "background-color:#fff;"
    return style

# --- 렌더링 ---
st.write("👇 빈 칸에 숫자(1~9)를 입력하세요")

table_html = "<table style='border-collapse: collapse;'>"
for i in range(9):
    table_html += "<tr>"
    for j in range(9):
        fixed_val = st.session_state.sudoku[i][j]
        solution_val = st.session_state.solution[i][j]
        key = f"cell_{i}_{j}"

        if fixed_val != 0:
            style = get_cell_style(i, j, is_fixed=True)
            table_html += f"<td style='{style}'>{fixed_val}</td>"
        else:
            user_val = st.session_state.user_input[i][j]
            input_val = st.text_input("", value=user_val, key=key, max_chars=1, label_visibility="collapsed")

            # 숫자 필터
            if input_val in "123456789":
                st.session_state.user_input[i][j] = input_val
            elif input_val == "":
                st.session_state.user_input[i][j] = ""
            else:
                input_val = ""

            # 오답일 경우 스타일 다르게
            is_wrong = False
            if st.session_state.checked:
                if input_val != str(solution_val):
                    is_wrong = True

            style = get_cell_style(i, j, is_fixed=False, is_wrong=is_wrong)
            table_html += f"<td style='{style}'>{input_val}</td>"

    table_html += "</tr>"
table_html += "</table>"

st.markdown(table_html, unsafe_allow_html=True)

# --- 정답 확인 ---
if st.button("✅ 정답 확인"):
    st.session_state.checked = True
    incorrect = False
    for i in range(9):
        for j in range(9):
            if st.session_state.sudoku[i][j] == 0:
                user_val = st.session_state.user_input[i][j]
                if user_val != str(st.session_state.solution[i][j]):
                    incorrect = True
    if incorrect:
        st.error("❌ 틀린 칸이 있어요. 다시 확인해보세요!")
    else:
        st.success("🎉 정답입니다! 잘했어요.")
