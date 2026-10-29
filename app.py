import json
import os
import re
import unicodedata
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="English 7 – Mid-term Revision",
    page_icon="📘",
    layout="wide",
)

# ---------------------------------------------------------------------
# QUESTION BANK transcribed from REVISION giữa hk1.docx.
# Correct answers are indexed from 0 (A=0, B=1, C=2).
# Questions with uncertain lost underline formatting are flagged below.
# ---------------------------------------------------------------------
MCQ = [
    {"part":"Revision 1", "section":"Choose the best answer", "q":"Your house is very .......... Hoa.", "opts":["nice","kind","helpful"], "ans":0},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"I love your dollhouse. It's ...........", "opts":["generous","difficult","amazing"], "ans":2},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"My hobby .......... building dollhouse.", "opts":["is","does","live"], "ans":0},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"I .......... to the Rider's club every Sunday.", "opts":["went","go","am going"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"I'd love to go to your club this Sunday. I want to learn how ...........", "opts":["ride","riding","to ride"], "ans":2},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"My dad has a big bookshelf because he loves .......... old books.", "opts":["making","doing","collecting"], "ans":2},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"Does your brother like .......... models?", "opts":["making","make","makes"], "ans":0},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"My mom enjoys .......... yoga every day to keep fit.", "opts":["to do","doing","do"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"My sister likes .......... camping at the weekend.", "opts":["doing","going","making"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"She .......... a drawing lesson every Tuesday.", "opts":["have","has","having"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"Mark doesn't .......... doing judo.", "opts":["like","to like","liking"], "ans":0},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"I don't want to get sunburn. Wear a .......... and use suncream.", "opts":["bag","hat","book"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"It's really hot and sunny at noon, so you might get ...........", "opts":["headache","flu","sunburn"], "ans":2},
    {"part":"Revision 1", "section":"Choose the best answer", "q":".......... are not good for your health.", "opts":["vegetables","soft drinks","fruits"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"We are not cleaning .......... our community library.", "opts":["up","on","at"], "ans":0},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"We .......... much fast food.", "opts":["aren't eat","don't eat","isn't eat"], "ans":1},
    {"part":"Revision 1", "section":"Pronunciation", "q":"Find the word which has a different sound in the underlined part: yoga / amazing / donate.", "opts":["yoga","amazing","donate"], "ans":2, "review":True},
    {"part":"Revision 1", "section":"Pronunciation", "q":"Find the word which has a different sound in the underlined part: developed / planted / needed.", "opts":["developed","planted","needed"], "ans":0},
    {"part":"Revision 1", "section":"Word stress", "q":"Find the word which has a different stress.", "opts":["donate","provide","volunteer"], "ans":2},
    {"part":"Revision 1", "section":"Word stress", "q":"Find the word which has a different stress.", "opts":["community","service","homeless"], "ans":0},
    {"part":"Revision 1", "section":"Error correction", "q":"Choose the underlined word or phrase that needs correcting: “Hoa grow vegetables in the school garden last summer.”", "opts":["A — Hoa","B — grow","C — last summer"], "ans":1},
    {"part":"Revision 1", "section":"Error correction", "q":"Choose the underlined word or phrase that needs correcting: “Peter didn't joined Lending Hand in 2015.”", "opts":["A — didn't","B — joined","C — in 2015"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"Children .......... plastic bottles for recycling a month ago.", "opts":["are collecting","collect","collected"], "ans":2},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"Yesterday, we .......... around our area and recycled them.", "opts":["donated food","picked up bottles","watered plants"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"We .......... English to children in a primary school last summer.", "opts":["are teaching","taught","teach"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"We pick up .......... at the local park every Sunday.", "opts":["water","litter","plant"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"Minh and his friends often .......... small children in their village.", "opts":["collect","donate","tutor"], "ans":2},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"To be a master in horse riding, you need to be very ...........", "opts":["strong","patient","careless"], "ans":1},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"Consuming lots of unhealthy food can lead to ...........", "opts":["sunburn","fitness","acne"], "ans":2},
    {"part":"Revision 1", "section":"Choose the best answer", "q":"Community service allows students to .......... themselves.", "opts":["develop","perform","exchange"], "ans":0},

    {"part":"Revision 2", "section":"Choose the best answer", "q":"She enjoys .......... board games at the weekend with his friends.", "opts":["playing","play","to play"], "ans":0},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"When she has spare time, she usually .......... swimming.", "opts":["go","goes","went"], "ans":1},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"They often .......... vegetables to a nursery school in the village.", "opts":["donating","donated","donate"], "ans":2},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"Last summer, we .......... a Paper-Notebook Exchange programme.", "opts":["started","start","starts"], "ans":0},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"We .......... for old people 2 days ago.", "opts":["sing","sang","singing"], "ans":1},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"We should .......... our surroundings clean.", "opts":["keeping","kept","keep"], "ans":2},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"We collect old books and .......... them for street children.", "opts":["protect","donate","exchange"], "ans":1},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"We .......... up litter around our area and recycled them 2 days ago.", "opts":["picked","donated","helped"], "ans":0},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"There are many ways to .......... money for charity.", "opts":["recycle","buy","raise"], "ans":2},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"You have a flu. You should .......... in bed and take a rest.", "opts":["stay","stays","stayed"], "ans":0},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"Tom hates .......... fast food because it is not healthy.", "opts":["eat","eating","ate"], "ans":1},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"Reading books in .......... can make your eyes tired and hurt your vision.", "opts":["red spots","chapped lips","dim light"], "ans":2},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"My aunt does not eat meat or fish because she is ...........", "opts":["an actor","a vegetarian","a farmer"], "ans":1},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"My brother usually .......... badminton with his friends after school.", "opts":["play","plays","played"], "ans":1},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"My sister .......... a lot of old books to the library yesterday.", "opts":["donated","donates","donate"], "ans":0},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"Lan: Last week, we provided food for homeless children in Ha Noi. Kim: “..........”", "opts":["I didn't enjoy it.","Wonderful!","I don't agree with you."], "ans":1},
    {"part":"Revision 2", "section":"Choose the best answer", "q":"Lan: “Do you enjoy collecting dolls in your free time?” Mai: “..........”", "opts":["Yes, I love it very much.","I went there yesterday.","You should sleep more."], "ans":0},
    {"part":"Revision 2", "section":"Word stress", "q":"Which main stress is placed differently from the others?", "opts":["model","collect","donate"], "ans":0},
    {"part":"Revision 2", "section":"Pronunciation", "q":"Which underlined part is pronounced differently from the others: washed / decided / cooked.", "opts":["washed","decided","cooked"], "ans":1},
]

WRITTEN = [
    {"part":"Revision 1", "section":"Put the words in the correct order", "prompt":"do / what / does / Lan / her free time / in /?", "answers":["What does Lan do in her free time?"]},
    {"part":"Revision 1", "section":"Put the words in the correct order", "prompt":"have / they / for breakfast / bread and eggs /.", "answers":["They have bread and eggs for breakfast."]},
    {"part":"Revision 1", "section":"Put the words in the correct order", "prompt":"likes / my sister / at the weekend / camping /.", "answers":["My sister likes camping at the weekend."]},
    {"part":"Revision 1", "section":"Put the words in the correct order", "prompt":"helped / we / in a village / the elderly / last summer /.", "answers":["We helped the elderly in a village last summer."]},
    {"part":"Revision 1", "section":"Write complete sentences", "prompt":"Hoa doesn't like / go / swimming / winter.", "answers":["Hoa doesn't like going swimming in winter.","Hoa doesn't like going swimming in the winter."]},
    {"part":"Revision 1", "section":"Write complete sentences", "prompt":"Nam / play / badminton / every day / after school.", "answers":["Nam plays badminton every day after school."]},
    {"part":"Revision 1", "section":"Write complete sentences", "prompt":"I / teach / three children in grade 1 / last summer.", "answers":["I taught three children in grade 1 last summer."]},
    {"part":"Revision 1", "section":"Write complete sentences", "prompt":"you / make / model / at / weekend?", "answers":["Do you make models at the weekend?","Do you make a model at the weekend?","Do you make models at the weekend"]},
    {"part":"Revision 2", "section":"Reorder the words/phrases", "prompt":"enjoys / My brother / with his friends / playing soccer /.", "answers":["My brother enjoys playing soccer with his friends."]},
    {"part":"Revision 2", "section":"Reorder the words/phrases", "prompt":"join / community activities / once a month / We /.", "answers":["We join community activities once a month."]},
    {"part":"Revision 2", "section":"Reorder the words/phrases", "prompt":"litter / often picks up / She / in the schoolyard /.", "answers":["She often picks up litter in the schoolyard."]},
    {"part":"Revision 2", "section":"Reorder the words/phrases", "prompt":"should / and sweetened food / Children / avoid / soft drinks /.", "answers":["Children should avoid soft drinks and sweetened food."]},
    {"part":"Revision 2", "section":"Reorder the words/phrases", "prompt":"last week / They / in the park / planted trees /.", "answers":["They planted trees in the park last week."]},
    {"part":"Revision 2", "section":"Reorder the words/phrases", "prompt":"drinks / my brother / never / milk tea /.", "answers":["My brother never drinks milk tea."]},
    {"part":"Revision 2", "section":"Reorder the words/phrases", "prompt":"much junk food / eat / children / shouldn't /.", "answers":["Children shouldn't eat much junk food."]},
    {"part":"Revision 2", "section":"Reorder the words/phrases", "prompt":"good / fresh vegetables / for your health / are /.", "answers":["Fresh vegetables are good for your health."]},
]

HEADERS = [
    "timestamp_vietnam", "attempt_id", "student_name", "class_name",
    "mcq_correct", "mcq_total", "written_correct", "written_total",
    "total_correct", "total_questions", "percent", "mcq_answers_json",
    "written_answers_json", "review_flags"
]

def normalize_answer(value):
    value = unicodedata.normalize("NFKC", value or "").lower().strip()
    value = value.replace("’", "'")
    value = re.sub(r"[.!?;,]+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value

def save_to_google_sheets(record):
    """Append one attempt to Google Sheets if secrets are configured."""
    import gspread
    from google.oauth2.service_account import Credentials

    if "gcp_service_account" not in st.secrets or "spreadsheet_id" not in st.secrets:
        return False, "Google Sheets chưa được cấu hình trong Streamlit Secrets."

    credentials_info = dict(st.secrets["gcp_service_account"])
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(st.secrets["spreadsheet_id"])

    try:
        worksheet = spreadsheet.worksheet("KetQua")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="KetQua", rows=2000, cols=len(HEADERS) + 2)

    if not worksheet.get_all_values():
        worksheet.append_row(HEADERS, value_input_option="USER_ENTERED")

    row = [record.get(header, "") for header in HEADERS]
    worksheet.append_row(row, value_input_option="USER_ENTERED")
    return True, "Google Sheets"

def save_local_csv(record):
    path = "ket_qua_english7.csv"
    new_df = pd.DataFrame([record])
    if os.path.exists(path):
        try:
            old_df = pd.read_csv(path)
            pd.concat([old_df, new_df], ignore_index=True).to_csv(path, index=False, encoding="utf-8-sig")
        except Exception:
            new_df.to_csv(path, index=False, encoding="utf-8-sig")
    else:
        new_df.to_csv(path, index=False, encoding="utf-8-sig")

st.title("📘 ENGLISH 7 – MID-TERM REVISION")
st.write("Ôn tập trực tuyến • Chấm điểm tự động • Lưu từng lượt làm")

with st.sidebar:
    st.header("Thông tin học sinh")
    student_name = st.text_input("Họ và tên", placeholder="Nhập họ tên")
    class_name = st.text_input("Lớp", placeholder="Ví dụ: 7/1")
    st.divider()
    st.caption("Em có thể làm bài nhiều lần. Mỗi lần nộp sẽ được ghi thành một lượt riêng.")

st.info("Bài gồm 49 câu trắc nghiệm và 16 câu viết. Hãy đọc kỹ câu hỏi trước khi nộp bài.")

with st.form("english7_full_test", clear_on_submit=False):
    st.header("PHẦN A – TRẮC NGHIỆM")
    st.caption("Mỗi câu đúng được 1 điểm. Chưa chọn đáp án thì câu đó được tính 0 điểm.")
    mcq_responses = {}
    current_part = None
    current_section = None
    for i, item in enumerate(MCQ):
        if item["part"] != current_part:
            current_part = item["part"]
            st.subheader(current_part)
            current_section = None
        if item["section"] != current_section:
            current_section = item["section"]
            st.markdown(f"**{current_section}**")
        labels = ["A", "B", "C"]
        choices = [f"{labels[j]}. {opt}" for j, opt in enumerate(item["opts"])]
        mcq_responses[str(i + 1)] = st.radio(
            f"Câu {i + 1}. {item['q']}",
            choices,
            index=None,
            key=f"mcq_{i}",
            label_visibility="visible",
        )

    st.divider()
    st.header("PHẦN B – VIẾT CÂU")
    st.caption("Mỗi câu đúng hoàn toàn được 1 điểm. Hệ thống so khớp với đáp án mẫu; câu diễn đạt khác có thể cần giáo viên xem lại.")
    written_responses = {}
    current_part = None
    current_section = None
    for i, item in enumerate(WRITTEN):
        if item["part"] != current_part:
            current_part = item["part"]
            st.subheader(current_part)
            current_section = None
        if item["section"] != current_section:
            current_section = item["section"]
            st.markdown(f"**{current_section}**")
        st.markdown(f"**Câu {i + 1}.** `{item['prompt']}`")
        written_responses[str(i + 1)] = st.text_input(
            "Viết câu hoàn chỉnh",
            key=f"written_{i}",
            placeholder="Nhập câu trả lời",
        )

    submitted = st.form_submit_button("NỘP BÀI VÀ CHẤM ĐIỂM", type="primary", use_container_width=True)

if submitted:
    if not student_name.strip() or not class_name.strip():
        st.error("Em cần nhập họ tên và lớp ở thanh bên trước khi nộp bài. Các câu trả lời vẫn còn trên màn hình; hãy nhập thông tin rồi nộp lại.")
    else:
        mcq_score = 0
        mcq_review = []
        for i, item in enumerate(MCQ):
            selected = mcq_responses.get(str(i + 1))
            correct_label = ["A", "B", "C"][item["ans"]]
            correct_text = f"{correct_label}. {item['opts'][item['ans']]}"
            is_correct = selected == correct_text
            mcq_score += int(is_correct)
            mcq_review.append({
                "number": i + 1,
                "question": item["q"],
                "selected": selected or "Chưa trả lời",
                "correct": correct_text,
                "is_correct": is_correct,
                "review": bool(item.get("review", False)),
            })

        written_score = 0
        written_review = []
        for i, item in enumerate(WRITTEN):
            response = written_responses.get(str(i + 1), "")
            accepted = {normalize_answer(a) for a in item["answers"]}
            is_correct = normalize_answer(response) in accepted
            written_score += int(is_correct)
            written_review.append({
                "number": i + 1,
                "prompt": item["prompt"],
                "response": response,
                "accepted": item["answers"][0],
                "is_correct": is_correct,
            })

        total_correct = mcq_score + written_score
        total_questions = len(MCQ) + len(WRITTEN)
        percent = round(total_correct / total_questions * 100, 2)
        attempt_id = str(uuid.uuid4())[:8].upper()
        now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%Y-%m-%d %H:%M:%S")
        review_flags = "Câu phát âm 17 cần rà soát gạch chân trong đề gốc" if any(x.get("review") for x in mcq_review) else ""

        record = {
            "timestamp_vietnam": now,
            "attempt_id": attempt_id,
            "student_name": student_name.strip(),
            "class_name": class_name.strip(),
            "mcq_correct": mcq_score,
            "mcq_total": len(MCQ),
            "written_correct": written_score,
            "written_total": len(WRITTEN),
            "total_correct": total_correct,
            "total_questions": total_questions,
            "percent": percent,
            "mcq_answers_json": json.dumps(mcq_responses, ensure_ascii=False),
            "written_answers_json": json.dumps(written_responses, ensure_ascii=False),
            "review_flags": review_flags,
        }
        st.session_state["last_result"] = {
            "record": record,
            "mcq_review": mcq_review,
            "written_review": written_review,
        }

        # Save every submission as a separate attempt.
        saved_to_sheets = False
        sheets_message = ""
        try:
            saved_to_sheets, sheets_message = save_to_google_sheets(record)
        except Exception as exc:
            sheets_message = f"Không thể ghi vào Google Sheets: {exc}"

        if saved_to_sheets:
            st.session_state["save_status"] = ("success", "Đã lưu lượt làm vào Google Sheets.")
        else:
            try:
                save_local_csv(record)
                st.session_state["save_status"] = ("warning", f"{sheets_message} Đã lưu dự phòng vào tệp CSV của ứng dụng. Trên Streamlit Cloud, CSV không bảo đảm tồn tại sau khi ứng dụng khởi động lại.")
            except Exception as exc:
                st.session_state["save_status"] = ("error", f"{sheets_message} Đồng thời không lưu được CSV dự phòng: {exc}")

if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    record = result["record"]
    st.divider()
    st.header("📊 KẾT QUẢ BÀI LÀM")
    c1, c2, c3 = st.columns(3)
    c1.metric("Trắc nghiệm", f"{record['mcq_correct']}/{record['mcq_total']}")
    c2.metric("Viết câu", f"{record['written_correct']}/{record['written_total']}")
    c3.metric("Tổng điểm", f"{record['total_correct']}/{record['total_questions']}", f"{record['percent']}%")
    st.write(f"**Học sinh:** {record['student_name']}  ·  **Lớp:** {record['class_name']}")
    st.write(f"**Mã lượt làm:** {record['attempt_id']}  ·  **Thời gian:** {record['timestamp_vietnam']}")
    status_kind, status_text = st.session_state.get("save_status", ("warning", "Chưa xác định trạng thái lưu."))
    if status_kind == "success":
        st.success(status_text)
    elif status_kind == "error":
        st.error(status_text)
    else:
        st.warning(status_text)

    with st.expander("Xem đáp án trắc nghiệm"):
        for item in result["mcq_review"]:
            symbol = "✅" if item["is_correct"] else "❌"
            st.markdown(f"{symbol} **Câu {item['number']}.** {item['question']}")
            st.write(f"Em chọn: {item['selected']}  |  Đáp án mẫu: {item['correct']}")
            if item["review"]:
                st.caption("Lưu ý: cần kiểm tra phần gạch chân trong bản Word gốc để xác nhận đáp án câu phát âm này.")

    with st.expander("Xem đáp án phần viết"):
        for item in result["written_review"]:
            symbol = "✅" if item["is_correct"] else "❌"
            st.markdown(f"{symbol} **Câu {item['number']}.** {item['prompt']}")
            st.write(f"Em trả lời: {item['response'] or 'Chưa trả lời'}")
            if not item["is_correct"]:
                st.write(f"Đáp án tham khảo: {item['accepted']}")

    st.caption("Muốn làm lại, em có thể chỉnh sửa câu trả lời phía trên rồi nhấn NỘP BÀI VÀ CHẤM ĐIỂM lần nữa. Mỗi lần nộp được lưu thành một lượt riêng.")

with st.expander("Hướng dẫn dành cho giáo viên: cấu hình Google Sheets"):
    st.markdown("""
1. Tạo một Google Sheet trống.
2. Tạo Google Cloud **Service Account**, bật Google Sheets API và Google Drive API, rồi tạo khóa JSON.
3. Chia sẻ Google Sheet cho email `client_email` của Service Account với quyền **Editor**.
4. Trong Streamlit Community Cloud, mở **App settings → Secrets** và thêm cấu hình theo file `secrets.toml.example`.
5. Khởi động lại ứng dụng. Ứng dụng sẽ tự tạo trang tính `KetQua` và thêm một dòng cho mỗi lần nộp bài.

Không đưa khóa JSON hoặc nội dung Secrets lên GitHub công khai.
""")

st.caption("Ứng dụng ôn tập dựa trên REVISION giữa hk1.docx. Giáo viên nên rà soát đáp án, đặc biệt câu phát âm có định dạng gạch chân, trước khi dùng chính thức.")
