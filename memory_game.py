import streamlit as st
import numpy as np
import random
import copy

st.set_page_config(page_title="스도쿠", layout="centered")
st.title("🧩 종이 느낌 스도쿠")

# --- 스도쿠 생성 ---
def is_valid(board, row, col, num):
    if num in board[row] or num in board[:, col]:
        return False
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    if num in board[sr:sr+3, sc:sc+3]:
        return False
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

# --- 새 게임 ---
if st.button("🔁 새 퍼즐 생성"):
    puzzle, solution = generate_sudoku(clues=35)
    st.session_state.sudoku = puzzle
    st.session_state.solution = solution
    st.session_state.user_input = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.checked = False
    st.rerun()

# --- 테이블 렌더링 ---
st.write("👇 숫자(1~9)를 직접 입력해보세요")

table_html = """
<style>
table {
    border-collapse: collapse;
    margin-top: 10px;
}
td {
    width: 45px;
    height: 45px;
    text-align: center;
    vertical-align: middle;
    font-size: 20px;
    font-family: monospace;
    border: 1px solid black;
}
td.fixed {
    background-color: #ddd;
}
td.incorrect {
    background-color: #ffdddd;
}
td.correct {
    background-color: #ddffdd;
}
td:nth-child(3), td:nth-child(6) {
    border-right: 3px solid black;
}
tr:nth-child(3) td, tr:nth-child(6) td {
    border-bottom: 3px solid black;
}
</style>
<table>
"""

for i in range(9):
    table_html += "<tr>"
    for j in range(9):
        val = st.session_state.sudoku[i][j]
        key = f"cell_{i}_{j}"
        if val != 0:
            table_html += f"<td class='fixed'>{val}</td>"
        else:
            user_val = st.session_state.user_input[i][j]
            input_val = st.text_input("", value=user_val, key=key, max_chars=1, label_visibility="collapsed")

            # 유효한 값만 반영
            if input_val in "123456789":
                st.session_state.user_input[i][j] = input_val
            elif input_val == "":
                st.session_state.user_input[i][j] = ""
            else:
                st.session_state.user_input[i][j] = ""

            # 정답 확인 시 표시
            css_class = ""
            if st.session_state.checked:
                correct_val = str(st.session_state.solution[i][j])
                if input_val == correct_val:
                    css_class = "correct"
                else:
                    css_class = "incorrect"

            table_html += f"<td class='{css_class}'>{input_val}</td>"
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
                u = st.session_state.user_input[i][j]
                if u != str(st.session_state.solution[i][j]):
                    incorrect = True
    if incorrect:
        st.error("❌ 틀린 칸이 있어요. 다시 확인해보세요!")
    else:
        st.success("🎉 정답입니다! 퍼즐을 완료했어요.")
