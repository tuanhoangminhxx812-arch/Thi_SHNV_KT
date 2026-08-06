"""
Script chuyển đổi dữ liệu từ file Excel sang JSON.
Chạy 1 lần trên máy local để tạo file data.json.
"""
import pandas as pd
import json
import re
import os
import sys
import xlrd

# Fix encoding on Windows
sys.stdout.reconfigure(encoding='utf-8')


EXAM_FILES = {
    "Kế toán trưởng, Trưởng-Phó phòng": "data_ktt.xls",
    "Chuyên viên": "data_cv.xls",
}

# Files for Khối VP – each file maps to a topic (display name)
VP_DIR = "Khối VP"
VP_FILES = [
    # (filename, sheet_name_or_None, icon, display_name)
    # sheet_name=None means read the first (or only) sheet
    ("5.SHNV Hanh chinh VP 2026.xls", "NV Hành Chính VP (100)", "📋", "Hành chính Văn phòng"),
    ("5.SHNV Hanh chinh VP 2026.xls", "AT Thông Tin (20)", "🔒", "An toàn Thông tin"),
    ("5.SHNV Hanh chinh VP 2026.xls", "VH Doanh Nghiệp (30)", "🏢", "Văn hóa Doanh nghiệp"),
    ("1.20CauATTT-TongQuan.xlsx", None, "🛡️", "ATTT - Tổng quan"),
    ("2.Vănhóadoanhnghiệp 2026 final.xls", None, "🌟", "Văn hóa DN (đề thi)"),
]

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
    """Parse Q/A format (column 0 = 'Q' or 'A', column 1 = text, column 2 = 'X' for correct)."""
    questions = []
    current_q = None
    for _, row in df.iterrows():
        row_type = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        text = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        is_correct = str(row.iloc[2]).strip().upper() == "X" if pd.notna(row.iloc[2]) else False
        if row_type == "Q" and text:
            if current_q and current_q["answers"]:
                questions.append(current_q)
            current_q = {"question": text, "answers": [], "correct_idx": -1}
        elif row_type == "A" and text and current_q is not None:
            cleaned = re.sub(r'^[a-dA-D][\.\\)]\s*', '', text).strip()
            current_q["answers"].append(cleaned if cleaned else text)
            if is_correct:
                current_q["correct_idx"] = len(current_q["answers"]) - 1
    if current_q and current_q["answers"]:
        questions.append(current_q)
    return [q for q in questions if q["correct_idx"] >= 0]


def parse_sheet_stt(df):
    """Parse STT format (column 0 = number for question, a/b/c/d for answers,
    column 1 = text, column 2 = 'X' for correct answer).
    
    This format is used in some VP Excel sheets where:
    - Questions have a numeric STT (1.0, 2.0, ...) in column 0
    - Answers have a/b/c/d in column 0
    - Correct answer is marked with 'X' in column 2
    """
    questions = []
    current_q = None
    for _, row in df.iterrows():
        col0 = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        text = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        is_correct = str(row.iloc[2]).strip().upper() == "X" if len(row) > 2 and pd.notna(row.iloc[2]) else False

        # Skip header/empty rows
        if not col0 or not text:
            continue

        # Check if this row is a question (numeric STT like '1.0', '2.0', '10.0', etc.)
        is_question = False
        try:
            float(col0)
            is_question = True
        except ValueError:
            pass

        # Check if this row is an answer (a, b, c, d, etc.)
        is_answer = col0.lower() in ('a', 'b', 'c', 'd', 'e', 'f')

        if is_question and text:
            if current_q and current_q["answers"]:
                questions.append(current_q)
            # Clean question text: remove "Câu X:" prefix if present
            clean_text = re.sub(r'^Câu\s*\d+\s*:\s*', '', text).strip()
            current_q = {"question": clean_text, "answers": [], "correct_idx": -1}
        elif is_answer and text and current_q is not None:
            # Clean the answer text (remove trailing .0 for numeric answers)
            if text.endswith('.0') and text[:-2].isdigit():
                text = text[:-2]
            current_q["answers"].append(text)
            if is_correct:
                current_q["correct_idx"] = len(current_q["answers"]) - 1

    if current_q and current_q["answers"]:
        questions.append(current_q)
    return [q for q in questions if q["correct_idx"] >= 0]


def detect_format(df):
    """Detect whether the sheet uses Q/A format or STT (numeric) format.
    Returns 'qa' or 'stt'."""
    for _, row in df.iterrows():
        col0 = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        if col0 == "Q":
            return "qa"
        if col0 in ("STT", "Phân Loại", "PHÂN LOẠI"):
            continue
        try:
            float(col0)
            return "stt"
        except ValueError:
            if col0.lower() in ('a', 'b', 'c', 'd'):
                return "stt"
    return "qa"  # default


def get_visible_sheets(filepath):
    visible_sheets = set()
    try:
        book = xlrd.open_workbook(filepath)
        for i in range(book.nsheets):
            if book.sheet_by_index(i).visibility == 0:
                visible_sheets.add(book.sheet_names()[i])
    except Exception:
        xls = pd.ExcelFile(filepath)
        visible_sheets = set(xls.sheet_names)
    return visible_sheets


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_data = {}

    # ─── Existing exam files (Kế toán trưởng, Chuyên viên) ──────────
    for label, filename in EXAM_FILES.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"❌ Không tìm thấy file: {filepath}")
            continue

        visible_sheets = get_visible_sheets(filepath)
        xls = pd.ExcelFile(filepath)
        topics = {}

        for sheet_name in xls.sheet_names:
            if sheet_name not in visible_sheets:
                continue
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            questions = parse_sheet(df)
            if questions:
                if label == "Chuyên viên" and sheet_name == "KTT-130":
                    continue
                if label == "Kế toán trưởng, Trưởng-Phó phòng" and sheet_name == "CV-120":
                    continue
                info = TOPIC_INFO.get(sheet_name, ("", sheet_name))
                display_name = f"{info[0]} {info[1]}"
                topics[display_name] = questions
                print(f"  ✅ {display_name}: {len(questions)} câu hỏi")

        all_data[label] = topics
        print(f"📦 {label}: {len(topics)} chủ đề")

    # ─── Khối VP files ───────────────────────────────────────────────
    vp_dir = os.path.join(base_dir, VP_DIR)
    vp_topics = {}

    if os.path.exists(vp_dir):
        print(f"\n--- Đang xử lý Khối VP ---")
        for filename, sheet_name, icon, display_name in VP_FILES:
            filepath = os.path.join(vp_dir, filename)
            if not os.path.exists(filepath):
                print(f"  ❌ Không tìm thấy file: {filename}")
                continue

            try:
                if sheet_name:
                    df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
                else:
                    df = pd.read_excel(filepath, header=None)

                # Detect format and parse
                fmt = detect_format(df)
                if fmt == "qa":
                    questions = parse_sheet(df)
                else:
                    questions = parse_sheet_stt(df)

                if questions:
                    full_name = f"{icon} {display_name}"
                    # Avoid duplicates if same topic from different files
                    if full_name in vp_topics:
                        full_name = f"{icon} {display_name} ({len(questions)} câu)"
                    vp_topics[full_name] = questions
                    print(f"  ✅ {full_name}: {len(questions)} câu hỏi (format: {fmt})")
                else:
                    print(f"  ⚠️ {display_name}: Không tìm thấy câu hỏi hợp lệ")
            except Exception as e:
                print(f"  ❌ Lỗi khi xử lý {filename} / {sheet_name}: {e}")
                import traceback
                traceback.print_exc()

        all_data["Khối VP"] = vp_topics
        print(f"📦 Khối VP: {len(vp_topics)} chủ đề")
    else:
        print(f"⚠️ Không tìm thấy thư mục: {vp_dir}")

    # ─── Write output ────────────────────────────────────────────────
    output_path = os.path.join(base_dir, "data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    file_size = os.path.getsize(output_path) / 1024
    print(f"\n✅ Đã tạo data.json ({file_size:.1f} KB)")
    print(f"📍 Đường dẫn: {output_path}")


if __name__ == "__main__":
    main()
