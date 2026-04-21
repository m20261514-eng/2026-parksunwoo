import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc

matplotlib.rcParams["axes.unicode_minus"] = False
rc("font", family="DejaVu Sans")

st.set_page_config(page_title="성적 표현 프로그램", page_icon="📚", layout="centered")

st.title("📚 성적 표현 프로그램")
st.markdown("과목별 점수를 입력하면 학점과 GPA를 자동으로 계산해 드립니다.")

# ── 학점 변환 함수 ──────────────────────────────────────────────────────────────
def score_to_grade(score: float) -> tuple[str, float]:
    """점수(0‑100)를 한국 대학 일반 기준으로 등급과 평점으로 변환한다."""
    if score >= 95:
        return "A+", 4.5
    elif score >= 90:
        return "A0", 4.0
    elif score >= 85:
        return "B+", 3.5
    elif score >= 80:
        return "B0", 3.0
    elif score >= 75:
        return "C+", 2.5
    elif score >= 70:
        return "C0", 2.0
    elif score >= 65:
        return "D+", 1.5
    elif score >= 60:
        return "D0", 1.0
    else:
        return "F", 0.0


# ── 사이드바: 학생 정보 입력 ────────────────────────────────────────────────────
with st.sidebar:
    st.header("🎓 학생 정보")
    student_name = st.text_input("학생 이름", placeholder="홍길동")
    student_id = st.text_input("학번", placeholder="20261514")

    st.header("➕ 과목 추가")
    subject_name = st.text_input("과목명", placeholder="파이썬 프로그래밍")
    subject_credit = st.number_input("학점 수", min_value=1, max_value=4, value=3, step=1)
    subject_score = st.number_input("점수 (0 ~ 100)", min_value=0.0, max_value=100.0, value=80.0, step=0.5)

    add_btn = st.button("과목 추가", use_container_width=True, type="primary")

# ── 세션 상태 초기화 ────────────────────────────────────────────────────────────
if "subjects" not in st.session_state:
    st.session_state.subjects = []

# ── 과목 추가 처리 ──────────────────────────────────────────────────────────────
if add_btn:
    if not subject_name.strip():
        st.sidebar.error("과목명을 입력해 주세요.")
    else:
        grade, points = score_to_grade(subject_score)
        st.session_state.subjects.append(
            {
                "과목명": subject_name.strip(),
                "학점": subject_credit,
                "점수": subject_score,
                "등급": grade,
                "평점": points,
            }
        )
        st.sidebar.success(f"'{subject_name.strip()}' 과목이 추가되었습니다.")

# ── 메인 영역 ───────────────────────────────────────────────────────────────────
if student_name or student_id:
    info_parts = []
    if student_name:
        info_parts.append(f"**학생:** {student_name}")
    if student_id:
        info_parts.append(f"**학번:** {student_id}")
    st.info("  |  ".join(info_parts))

if not st.session_state.subjects:
    st.markdown(
        """
        > 왼쪽 사이드바에서 과목명, 학점 수, 점수를 입력한 뒤 **과목 추가** 버튼을 눌러 성적을 등록하세요.
        """
    )
else:
    df = pd.DataFrame(st.session_state.subjects)

    # 삭제 버튼 ──────────────────────────────────────────────────────────────────
    col_table, col_del = st.columns([4, 1])
    with col_del:
        delete_idx = st.number_input(
            "삭제할 행 번호",
            min_value=1,
            max_value=len(df),
            value=1,
            step=1,
            label_visibility="collapsed",
        )
        if st.button("행 삭제", use_container_width=True):
            st.session_state.subjects.pop(int(delete_idx) - 1)
            st.rerun()

    with col_table:
        display_df = df.copy()
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df, use_container_width=True)

    # 전체 초기화 버튼 ────────────────────────────────────────────────────────────
    if st.button("전체 초기화", type="secondary"):
        st.session_state.subjects = []
        st.rerun()

    # ── GPA / 통계 계산 ──────────────────────────────────────────────────────────
    total_credits = df["학점"].sum()
    weighted_points = (df["평점"] * df["학점"]).sum()
    gpa = weighted_points / total_credits if total_credits > 0 else 0.0
    avg_score = df["점수"].mean()

    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 이수 학점", f"{total_credits} 학점")
    col2.metric("평균 점수", f"{avg_score:.2f}점")
    col3.metric("GPA", f"{gpa:.2f} / 4.5")
    col4.metric("과목 수", f"{len(df)}개")

    # ── 시각화 ───────────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📊 과목별 점수 시각화")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # 막대 그래프: 점수
    colors = []
    for score in df["점수"]:
        if score >= 90:
            colors.append("#4CAF50")
        elif score >= 80:
            colors.append("#2196F3")
        elif score >= 70:
            colors.append("#FF9800")
        elif score >= 60:
            colors.append("#FF5722")
        else:
            colors.append("#9E9E9E")

    bars = axes[0].bar(df["과목명"], df["점수"], color=colors, edgecolor="white", linewidth=0.8)
    axes[0].set_ylim(0, 110)
    axes[0].set_ylabel("점수")
    axes[0].set_title("과목별 점수")
    axes[0].axhline(y=avg_score, color="red", linestyle="--", linewidth=1.2, label=f"평균 {avg_score:.1f}점")
    axes[0].legend(fontsize=9)
    for bar, score in zip(bars, df["점수"]):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{score:.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=30, ha="right", fontsize=9)

    # 파이 차트: 등급 분포
    grade_counts = df["등급"].value_counts()
    grade_colors = {
        "A+": "#1B5E20", "A0": "#4CAF50",
        "B+": "#0D47A1", "B0": "#2196F3",
        "C+": "#E65100", "C0": "#FF9800",
        "D+": "#BF360C", "D0": "#FF5722",
        "F": "#9E9E9E",
    }
    pie_colors = [grade_colors.get(g, "#BDBDBD") for g in grade_counts.index]
    axes[1].pie(
        grade_counts.values,
        labels=grade_counts.index,
        colors=pie_colors,
        autopct="%1.0f%%",
        startangle=90,
        textprops={"fontsize": 10},
    )
    axes[1].set_title("등급 분포")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # ── 등급 범례 ────────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📋 등급 기준표")
    grade_table = pd.DataFrame(
        {
            "등급": ["A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F"],
            "점수 범위": ["95 ~ 100", "90 ~ 94", "85 ~ 89", "80 ~ 84", "75 ~ 79", "70 ~ 74", "65 ~ 69", "60 ~ 64", "0 ~ 59"],
            "평점": [4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.0],
        }
    )
    st.dataframe(grade_table, use_container_width=True, hide_index=True)
