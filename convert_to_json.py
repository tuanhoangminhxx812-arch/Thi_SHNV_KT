"""
Script chuyển đổi dữ liệu từ file Excel sang JSON.
Chạy 1 lần trên máy local để tạo file data.json.
"""
import pandas as pd
import json
import re
import os
import xlrd


EXAM_FILES = {
    "Kế toán trưởng, Trưởng-Phó phòng": "data_ktt.xls",
    "Chuyên viên": "data_cv.xls",
}

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

    output_path = os.path.join(base_dir, "data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    file_size = os.path.getsize(output_path) / 1024
    print(f"\n✅ Đã tạo data.json ({file_size:.1f} KB)")
    print(f"📍 Đường dẫn: {output_path}")


if __name__ == "__main__":
    main()
