import random
import pandas as pd
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 지옥의 랭킹전", page_icon="🎯", layout="centered"
)

# 세션 스테이트 초기화 (게임 데이터 유지용)
if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "ranking" not in st.session_state:
    # 기본 랭킹 데이터 (이름, 시도 횟수)
    st.session_state.ranking = pd.DataFrame(
        {
            "플레이어": ["AI 조교", "뉴턴", "할로"],
            "시도 횟수": [3, 5, 7],
        }
    )

st.title("🎯 1~100 숫자 맞추기 챌린지")
st.markdown("컴퓨터가 숨긴 1부터 100 사이의 숫자를 찾아내세요!")

# 사이드바: 랭킹판 보기
st.sidebar.title("🏆 명예의 전당 (Top 5)")
st.sidebar.markdown("시도 횟수가 적을수록 상위 랭크됩니다.")

# 랭킹 정렬 후 출력
sorted_ranking = st.session_state.ranking.sort_values(
    by="시도 횟수", ascending=True
).head(5)
st.sidebar.dataframe(sorted_ranking, hide_index=True)

if st.sidebar.button("🔄 랭킹 초기화"):
    st.session_state.ranking = pd.DataFrame(
        columns=["플레이어", "시도 횟수"]
    )
    st.rerun()

# 게임 플레이 영역
if not st.session_state.game_over:
    # 사용자 입력
    player_name = st.text_input("당신의 닉네임을 입력해주세요:", value="익명의 도전자")
    guess = st.number_input(
        "1부터 100 사이의 숫자를 입력하세요", min_value=1, max_value=100, step=1
    )

    if st.button("🚀 정답 제출!"):
        st.session_state.attempts += 1
        diff = abs(guess - st.session_state.target_number)

        if guess == st.session_state.target_number:
            st.session_state.game_over = True
            st.balloons()
            st.success(
                f"🎉 정답입니다! {st.session_state.attempts}번 만에 맞추셨습니다!"
            )

            # 랭킹에 결과 추가
            new_record = pd.DataFrame(
                {"플레이어": [player_name], "시도 횟수": [st.session_state.attempts]}
            )
            st.session_state.ranking = pd.concat(
                [st.session_state.ranking, new_record], ignore_index=True
            )

            st.rerun()
        else:
            # 센스 있는 도발 메시지 시스템
            if guess < st.session_state.target_number:
                msg = "📈 **UP!** 그것보다 **더 큰 숫자**입니다. 눈을 떠보세요!"
            else:
                msg = "📉 **DOWN!** 그것보다 **더 작은 숫자**입니다. 산으로 가고 있어요!"

            if diff <= 5:
                msg += " 🔥 아슬아슬합니다! 뜨거워지고 있어요!"
            elif diff >= 30:
                msg += " 🧊 영하권입니다. 너무 멀었어요!"

            st.warning(
                f"입력한 숫자: {guess} | {msg} (현재 {st.session_state.attempts}번째 도전 중)"
            )

else:
    st.info("게임이 종료되었습니다. 다시 도전하시겠습니까?")
    if st.button("🎮 판 다시 벌리기 (재시작)"):
        st.session_state.target_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.rerun()
