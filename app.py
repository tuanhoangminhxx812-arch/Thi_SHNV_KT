import streamlit as st
import pandas as pd
import random
import re
import os

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ôn Tập Trắc Nghiệm - SHNV Tài Chính Kế Toán",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Font fallback + Times New Roman */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap');

    /* Global font - Force Times New Roman everywhere */
    * {
        font-family: 'Times New Roman', Times, Georgia, serif !important;
    }
    html, body, [class*="css"], .stMarkdown, .stRadio label,
    .stSelectbox, .stTextInput input,
    p, span, div, li, label, input, select, textarea,
    [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
    .st-emotion-cache-16idsys p, .st-emotion-cache-1629p8f,
    .element-container, .stRadio div[role="radiogroup"] label {
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-size: 16px !important;
    }

    /* Hide Streamlit branding and header space */
    [data-testid="stHeader"] {
        display: none !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e0e0;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e0e0e0 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #c0c0c0 !important;
    }
    section[data-testid="stSidebar"] label {
        color: #e0e0e0 !important;
    }

    /* Main content area - widened and shifted up to maximize viewport usage */
    .main .block-container {
        max-width: 1250px !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
    }

    /* 3D Topic Card Buttons - main content area */
    .main .topic-btn-row .stButton > button {
        background: linear-gradient(145deg, #ffffff, #f0f2ff) !important;
        border-radius: 20px !important;
        padding: 1rem 0.8rem !important;
        min-height: 220px !important;
        color: #1a1a2e !important;
        border: 1px solid rgba(200, 210, 240, 0.6) !important;
        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.08),
            0 2px 6px rgba(0, 0, 0, 0.04),
            inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        transform-style: preserve-3d !important;
        white-space: pre-line !important;
        line-height: 1.5 !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .main .topic-btn-row .stButton > button p,
    .main .topic-btn-row .stButton > button span {
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
        line-height: 1.5 !important;
        text-align: center !important;
        margin: 0 !important;
        display: block !important;
        width: 100% !important;
    }
    /* Styles the first line (emoji icon) to be huge and prominent */
    .main .topic-btn-row .stButton > button p::first-line,
    .main .topic-btn-row .stButton > button span::first-line {
        font-size: 48px !important;
        line-height: 1.2 !important;
    }
    .main .topic-btn-row .stButton > button:hover {
        transform: translateY(-10px) rotateX(4deg) rotateY(-2deg) scale(1.03) !important;
        box-shadow:
            0 18px 36px rgba(102, 126, 234, 0.25),
            0 8px 14px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 1) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(145deg, #f8f9ff, #eef0ff) !important;
        color: #1a1a2e !important;
    }
    .main .topic-btn-row .stButton > button:active {
        transform: translateY(-4px) scale(1.01) !important;
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.2) !important;
    }
    .main .topic-btn-row {
        perspective: 800px;
        margin-bottom: 0.5rem;
    }

    /* Question card */
    .question-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border: 1px solid #e0e4f0;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    }
    .question-card h3 {
        color: #1a1a2e;
        font-size: 20px !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    .question-text {
        color: #2c3e50;
        font-size: 16px !important;
        line-height: 1.8;
        margin-bottom: 1rem;
    }

    /* Question number badge */
    .q-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 14px !important;
        font-weight: 600;
        margin-bottom: 12px;
    }

    /* Result cards */
    .result-correct {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        color: #155724 !important;
    }
    .result-correct p { color: #155724 !important; }

    .result-wrong {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        color: #721c24 !important;
    }
    .result-wrong p { color: #721c24 !important; }

    /* Score cards */
    .score-pass {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 8px 30px rgba(40, 167, 69, 0.3);
    }
    .score-pass h2, .score-pass h3, .score-pass p { color: white !important; }

    .score-fail {
        background: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 8px 30px rgba(220, 53, 69, 0.3);
    }
    .score-fail h2, .score-fail h3, .score-fail p { color: white !important; }

    /* Topic buttons in sidebar */
    .topic-item {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #e0e0e0 !important;
        cursor: pointer;
        transition: all 0.2s;
    }
    .topic-item:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateX(4px);
    }
    .topic-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: transparent !important;
        color: white !important;
    }

    /* Progress bar custom */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 10px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        border: none !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }

    /* Sidebar secondary buttons: dark text on white background */
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"],
    section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {
        color: #1a1a2e !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover,
    section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {
        background-color: rgba(255, 255, 255, 1) !important;
        color: #0f3460 !important;
    }
    /* Sidebar primary (active) button: white text */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        color: white !important;
    }

    /* Radio button styling */
    .stRadio > div {
        background: #f8f9ff;
        border-radius: 12px;
        padding: 0.8rem 1rem;
    }
    .stRadio label {
        font-size: 16px !important;
        padding: 6px 0 !important;
        line-height: 1.7 !important;
    }

    /* Stats cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px 16px;
        text-align: center;
        margin: 4px 0;
    }
    .stat-card p { color: #c0c0c0 !important; margin: 0; }
    .stat-value {
        font-size: 22px !important;
        font-weight: 700;
        color: #667eea !important;
    }

    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem 2.5rem 1.8rem;
        text-align: center;
        color: white !important;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    .welcome-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
        animation: shimmer 8s ease-in-out infinite;
    }
    @keyframes shimmer {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(30%, 30%); }
    }
    .welcome-banner h1, .welcome-banner h2, .welcome-banner p {
        color: white !important;
        position: relative;
        z-index: 1;
    }

    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        border: none;
        margin: 1.5rem 0;
    }

    /* Review table */
    .review-correct { color: #28a745 !important; font-weight: 600; }
    .review-wrong { color: #dc3545 !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ─── Data Loading ────────────────────────────────────────────────────────────
# Map file names to display labels
EXAM_FILES = {
    "Kế toán trưởng, Trưởng-Phó phòng": "Đề thi SHNV TCKT - 2025 09-02-2026_ kế toán trường, trưởng-phó phòng.xls",
    "Chuyên viên": "Đề thi SHNV TCKT - 2025 09-02-2026_chuyên viên.xls",
}

# Friendly topic names mapping: {sheet_name: (icon, display_name)}
TOPIC_INFO = {
    "KTT-130": ("📘", "KTT - 130 câu"),
    "CV-120": ("📗", "Chuyên viên - 120 câu"),
    "Tổng hợp": ("📚", "Tổng hợp"),
    "Thuế": ("💰", "Thuế"),
    "QC chi tieu noi bo": ("📋", "Quy chế chi tiêu nội bộ"),
    "Quản trị rủi ro": ("🛡️", "Quản trị rủi ro"),
    "ERP": ("💻", "ERP"),
    "kế toán": ("📊", "Kế toán"),
    "Chế độ kế toán- TT99": ("📑", "Chế độ kế toán - TT99"),
}


def parse_sheet(df):
    """Parse a single sheet DataFrame into a list of question dicts."""
    questions = []
    current_q = None

    for _, row in df.iterrows():
        row_type = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        text = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        is_correct = str(row.iloc[2]).strip().upper() == "X" if pd.notna(row.iloc[2]) else False

        if row_type == "Q" and text:
            # Save previous question if exists
            if current_q and current_q["answers"]:
                questions.append(current_q)
            current_q = {
                "question": text,
                "answers": [],
                "correct_idx": -1,
            }
        elif row_type == "A" and text and current_q is not None:
            # Strip existing answer prefix (a., b., c., d., A., etc.)
            cleaned = re.sub(r'^[a-dA-D][\.\)]\s*', '', text).strip()
            if cleaned:
                current_q["answers"].append(cleaned)
            else:
                current_q["answers"].append(text)
            if is_correct:
                current_q["correct_idx"] = len(current_q["answers"]) - 1

    # Don't forget the last question
    if current_q and current_q["answers"]:
        questions.append(current_q)

    # Filter out questions without a correct answer
    questions = [q for q in questions if q["correct_idx"] >= 0]
    return questions


@st.cache_data
def load_all_data():
    """Load and parse all exam data from both Excel files."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_data = {}

    for label, filename in EXAM_FILES.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            st.error(f"Không tìm thấy file: {filename}")
            continue

        xls = pd.ExcelFile(filepath)
        topics = {}
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            questions = parse_sheet(df)
            if questions:
                info = TOPIC_INFO.get(sheet_name, ("", sheet_name))
                display_name = f"{info[0]} {info[1]}"
                topics[display_name] = questions

        all_data[label] = topics

    return all_data


# ─── Session State Init ─────────────────────────────────────────────────────
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "audience": None,          # Selected audience
        "topic": None,             # Selected topic
        "questions": [],           # Shuffled questions for current topic
        "current_idx": 0,          # Current question index
        "score": 0,                # Number of correct answers
        "answered": False,         # Whether current question has been answered
        "selected_answer": None,   # User's selected answer
        "quiz_finished": False,    # Whether quiz is complete
        "answers_log": [],         # Log of all answers for review
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_quiz(audience, topic, questions):
    """Start a new quiz with shuffled questions."""
    shuffled = questions.copy()
    random.shuffle(shuffled)
    st.session_state.audience = audience
    st.session_state.topic = topic
    st.session_state.questions = shuffled
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.quiz_finished = False
    st.session_state.answers_log = []


def reset_quiz():
    """Reset to topic selection."""
    st.session_state.topic = None
    st.session_state.questions = []
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.quiz_finished = False
    st.session_state.answers_log = []


# ─── Main App ────────────────────────────────────────────────────────────────
def main():
    init_session_state()
    all_data = load_all_data()

    if not all_data:
        st.error("Không tải được dữ liệu từ file Excel. Vui lòng kiểm tra lại.")
        return

    # ─── Sidebar ─────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 📝 Ôn Tập SHNV")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Audience selection
        st.markdown("### 👤 Đối tượng thi")
        audience_options = list(all_data.keys())
        selected_audience = st.selectbox(
            "Chọn đối tượng:",
            audience_options,
            index=0,
            label_visibility="collapsed",
        )

        # Reset if audience changed
        if st.session_state.audience != selected_audience:
            st.session_state.audience = selected_audience
            reset_quiz()

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Topic selection
        if selected_audience in all_data:
            topics = all_data[selected_audience]
            st.markdown("### 📂 Chủ đề")

            for topic_name, topic_questions in topics.items():
                n_questions = len(topic_questions)
                is_active = st.session_state.topic == topic_name
                icon = "▶" if is_active else "○"
                label = f"{icon} {topic_name} ({n_questions} câu)"

                if st.button(
                    label,
                    key=f"topic_{topic_name}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    start_quiz(selected_audience, topic_name, topic_questions)
                    st.rerun()

            # Show progress if a quiz is active
            if st.session_state.topic and st.session_state.questions:
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown("### 📊 Tiến trình")

                total = len(st.session_state.questions)
                current = st.session_state.current_idx
                if st.session_state.quiz_finished:
                    current = total

                st.progress(current / total if total > 0 else 0)
                st.markdown(f"""
                <div class="stat-card">
                    <p>Câu hỏi</p>
                    <p class="stat-value">{current} / {total}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="stat-card">
                    <p>Đúng</p>
                    <p class="stat-value" style="color: #28a745 !important;">
                        {st.session_state.score} ✓
                    </p>
                </div>
                """, unsafe_allow_html=True)

                answered_count = len(st.session_state.answers_log)
                wrong = answered_count - st.session_state.score
                st.markdown(f"""
                <div class="stat-card">
                    <p>Sai</p>
                    <p class="stat-value" style="color: #dc3545 !important;">
                        {wrong} ✗
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Reset button
                st.markdown("")
                if st.button("🔄 Làm lại", use_container_width=True):
                    topic_qs = topics.get(st.session_state.topic, [])
                    start_quiz(selected_audience, st.session_state.topic, topic_qs)
                    st.rerun()

    # ─── Main Content ────────────────────────────────────────────────────
    if not st.session_state.topic:
        #Welcome screen
        st.markdown("""
        <div class="welcome-banner">
            <h1 style="font-size: 72px !important; margin-top: 0px !important; margin-bottom: 0.4rem !important; font-weight: 700; line-height: 1.1;">
                📝 Ôn Tập Trắc Nghiệm
            </h1>
            <h2 style="font-size: 34px !important; font-weight: 400; margin-top: 0px !important; margin-bottom: 0.4rem !important; line-height: 1.2;">
                Sát Hạch Nghiệp Vụ — Tài Chính Kế Toán
            </h2>
            <p style="font-size: 22px !important; opacity: 0.95; margin: 0px !important; line-height: 1.3;">
                👈 Chọn đối tượng thi và chủ đề bên dưới hoặc thanh bên trái để bắt đầu
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Display topic overview as clickable 3D card-buttons
        if selected_audience in all_data:
            topics = all_data[selected_audience]
            st.markdown(f'<h3 style="font-size: 24px !important; color: #1a1a2e; margin-top: 0.5rem !important; margin-bottom: 0.6rem !important;">📋 Chọn chủ đề — {selected_audience}</h3>', unsafe_allow_html=True)

            # Render 3 rows of 3 cards
            topic_list = list(topics.items())
            for row_start in range(0, len(topic_list), 3):
                row_items = topic_list[row_start:row_start + 3]
                cols = st.columns(3)
                for col_idx, (topic_name, topic_qs) in enumerate(row_items):
                    parts = topic_name.split(" ", 1)
                    icon = parts[0] if len(parts) > 1 else "📄"
                    name = parts[1] if len(parts) > 1 else topic_name

                    with cols[col_idx]:
                        st.markdown('<div class="topic-btn-row">', unsafe_allow_html=True)
                        btn_label = f"{icon}\n{name}\n{len(topic_qs)} câu hỏi"
                        if st.button(btn_label, key=f"start_{topic_name}", use_container_width=True):
                            start_quiz(selected_audience, topic_name, topic_qs)
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

        return

    # ─── Quiz in progress ────────────────────────────────────────────────
    questions = st.session_state.questions
    total = len(questions)

    if st.session_state.quiz_finished:
        # ─── Results Screen ──────────────────────────────────────────
        score = st.session_state.score
        percentage = (score / total * 100) if total > 0 else 0
        passed = percentage >= 70

        # Score card
        css_class = "score-pass" if passed else "score-fail"
        result_text = "🎉 ĐẠT YÊU CẦU" if passed else "❌ CHƯA ĐẠT YÊU CẦU"
        emoji = "🏆" if passed else "📖"

        st.markdown(f"""
        <div class="{css_class}">
            <h2 style="font-size: 28px !important; margin-bottom: 0.5rem;">{result_text}</h2>
            <p style="font-size: 18px !important; margin-bottom: 1rem;">
                {st.session_state.topic}
            </p>
            <h3 style="font-size: 48px !important; margin: 0.5rem 0;">
                {emoji} {percentage:.1f}%
            </h3>
            <p style="font-size: 18px !important;">
                Trả lời đúng: {score} / {total} câu
            </p>
            <p style="font-size: 14px !important; opacity: 0.8;">
                Ngưỡng đạt: ≥ 70%
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Detailed review
        st.markdown("### 📋 Chi tiết bài làm")

        for i, log_entry in enumerate(st.session_state.answers_log):
            q = log_entry["question"]
            user_ans = log_entry["user_answer"]
            correct_ans = log_entry["correct_answer"]
            is_correct = log_entry["is_correct"]

            status_icon = "✅" if is_correct else "❌"
            status_class = "review-correct" if is_correct else "review-wrong"

            with st.expander(f"{status_icon} Câu {i + 1}: {q[:80]}{'...' if len(q) > 80 else ''}"):
                st.markdown(f"**Câu hỏi:** {q}")
                if is_correct:
                    st.markdown(f'<p class="review-correct">✅ Đáp án của bạn: {user_ans}</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="review-wrong">❌ Đáp án của bạn: {user_ans}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="review-correct">✅ Đáp án đúng: {correct_ans}</p>', unsafe_allow_html=True)

        # Action buttons
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Làm lại chủ đề này", use_container_width=True, type="primary"):
                topic_data = all_data.get(selected_audience, {})
                topic_qs = topic_data.get(st.session_state.topic, [])
                start_quiz(selected_audience, st.session_state.topic, topic_qs)
                st.rerun()
        with col2:
            if st.button("📂 Chọn chủ đề khác", use_container_width=True):
                reset_quiz()
                st.rerun()

        return

    # ─── Display Current Question ────────────────────────────────────
    idx = st.session_state.current_idx
    q = questions[idx]

    # Header
    st.markdown(f"""
    <div class="question-card">
        <span class="q-badge">Câu {idx + 1} / {total}</span>
        <h3>{q["question"]}</h3>
    </div>
    """, unsafe_allow_html=True)

    # Answer options
    if not st.session_state.answered:
        # Create answer labels with A, B, C, D prefixes
        labels = []
        prefix_letters = "ABCDEFGHIJKLMNOP"
        for i, ans in enumerate(q["answers"]):
            prefix = prefix_letters[i] if i < len(prefix_letters) else str(i + 1)
            labels.append(f"{prefix}. {ans}")

        selected = st.radio(
            "Chọn đáp án:",
            options=labels,
            index=None,
            key=f"radio_{idx}_{id(q)}",
            label_visibility="collapsed",
        )

        st.markdown("")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("✅ Trả lời", type="primary", use_container_width=True, disabled=(selected is None)):
                if selected is not None:
                    # Find which answer index was selected
                    selected_idx = labels.index(selected)
                    is_correct = selected_idx == q["correct_idx"]

                    st.session_state.answered = True
                    st.session_state.selected_answer = selected_idx

                    if is_correct:
                        st.session_state.score += 1

                    # Log the answer
                    correct_answer_text = q["answers"][q["correct_idx"]]
                    user_answer_text = q["answers"][selected_idx]
                    st.session_state.answers_log.append({
                        "question": q["question"],
                        "user_answer": user_answer_text,
                        "correct_answer": correct_answer_text,
                        "is_correct": is_correct,
                    })

                    st.rerun()

    else:
        # Show answers with correct/wrong highlighting
        selected_idx = st.session_state.selected_answer
        correct_idx = q["correct_idx"]
        is_correct = selected_idx == correct_idx
        prefix_letters = "ABCDEFGHIJKLMNOP"

        # Show feedback
        if is_correct:
            st.markdown(f"""
            <div class="result-correct">
                <p style="font-size: 18px !important; font-weight: 600;">
                    ✅ Chính xác!
                </p>
                <p>Đáp án: <strong>{prefix_letters[correct_idx]}. {q["answers"][correct_idx]}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-wrong">
                <p style="font-size: 18px !important; font-weight: 600;">
                    ❌ Sai rồi!
                </p>
                <p>Bạn chọn: <strong>{prefix_letters[selected_idx]}. {q["answers"][selected_idx]}</strong></p>
                <p>Đáp án đúng: <strong>{prefix_letters[correct_idx]}. {q["answers"][correct_idx]}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        # Show all answers with visual indicators
        for i, ans in enumerate(q["answers"]):
            prefix = prefix_letters[i] if i < len(prefix_letters) else str(i + 1)
            if i == correct_idx:
                st.markdown(f"✅ **{prefix}. {ans}**")
            elif i == selected_idx and not is_correct:
                st.markdown(f"❌ ~~{prefix}. {ans}~~")
            else:
                st.markdown(f"○ {prefix}. {ans}")

        # Next button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if idx < total - 1:
                if st.button("➡️ Câu tiếp theo", type="primary", use_container_width=True):
                    st.session_state.current_idx += 1
                    st.session_state.answered = False
                    st.session_state.selected_answer = None
                    st.rerun()
            else:
                if st.button("🏁 Xem kết quả", type="primary", use_container_width=True):
                    st.session_state.quiz_finished = True
                    st.rerun()


if __name__ == "__main__":
    main()
