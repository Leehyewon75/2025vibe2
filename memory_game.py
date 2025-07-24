import streamlit as st
import numpy as np
import random
import copy

st.set_page_config(page_title="스도쿠", layout="centered")
st.title("🧩 기능 + 예쁜 스도쿠 (columns 방식)")

# --- 퍼즐 생성 ---
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

# --- 새 게임 버튼 ---
if st.button("🔁 새 퍼즐 생성"):
    puzzle, solution = generate_sudoku(clues=35)
    st.session_state.sudoku = puzzle
    st.session_state.solution = solution
    st.session_state.user_input = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.checked = False
    st.rerun()

# --- 스타일 함수 ---
def get_style(i, j, fixed=False, correct=None):
    style = "text-align:center; font-size:20px; height:50px; width:50px;"
    style += "padding:6px; border-radius:4px; border:1px solid #ccc;"

    # 블록 경계선 강조
    if i % 3 == 0 and i != 0:
        style += "border-top: 3px solid black;"
    if j % 3 == 0 and j != 0:
        style += "border-left: 3px solid black;"

    if fixed:
        style += "background-color:#eee;"
    elif correct is True:
        style += "background-color:#cceedd;"
    elif correct is False:
        style += "background-color:#ffdddd;"
    else:
        style += "background-color:white;"

    return style

# --- UI 렌더링 ---
for i in range(9):
    cols = st.columns(9)
    for j in range(9):
        key = f"cell_{i}_{j}"
        fixed_val = st.session_state.sudoku[i][j]
        solution_val = st.session_state.solution[i][j]
        user_val = st.session_state.user_input[i][j]

        # 고정 숫자
        if fixed_val != 0:
            style = get_style(i, j, fixed=True)
            cols[j].markdown(f"<div style='{style}'>{fixed_val}</div>", unsafe_allow_html=True)
        else:
            # 유저 입력
            user_input = cols[j].text_input(
                "", user_val, max_chars=1, key=key, label_visibility="collapsed"
            )
            if user_input in "123456789":
                st.session_state.user_input[i][j] = user_input
            elif user_input == "":
                st.session_state.user_input[i][j] = ""
            else:
                st.session_state.user_input[i][j] = ""

# --- 정답 확인 버튼 ---
if st.button("✅ 정답 확인"):
    st.session_state.checked = True

# --- 정답 피드백 표시 (하이라이트만) ---
if st.session_state.checked:
    st.subheader("🔍 정답 결과")
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            val = st.session_state.sudoku[i][j]
            input_val = st.session_state.user_input[i][j]
            solution_val = str(st.session_state.solution[i][j])

            if val != 0:
                style = get_style(i, j, fixed=True)
                cols[j].markdown(f"<div style='{style}'>{val}</div>", unsafe_allow_html=True)
            else:
                correct = input_val == solution_val
                style = get_style(i, j, correct=correct)
                cols[j].markdown(f"<div style='{style}'>{input_val}</div>", unsafe_allow_html=True)

    # 결과 메시지
    all_correct = all(
        st.session_state.sudoku[i][j] != 0 or
        st.session_state.user_input[i][j] == str(st.session_state.solution[i][j])
        for i in range(9) for j in range(9)
    )
    if all_correct:
        st.success("🎉 정답입니다! 퍼즐을 완성했어요!")
    else:
        st.error("❌ 일부 칸이 틀렸어요. 다시 시도해보세요!")
