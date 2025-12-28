import streamlit as st
import openpyxl
from openpyxl.styles import PatternFill
from datetime import datetime, timedelta, time
import io

# إعداد الصفحة وتصميم الاستايل (CSS)
st.set_page_config(page_title="Youssef Pasha - The Ultimate Fix", layout="wide")

# تصميم الواجهة بالألوان المتوهجة (Neon Style)
st.markdown("""
    <style>
    /* خلفية الصفحة */
    .stApp {
        background-color: #0e1117;
    }
    /* تصميم العنوان الرئيسي */
    .main-title {
        text-align: center;
        color: #00f2ff;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
        padding: 20px;
    }
    /* تصميم صناديق الرفع */
    .stFileUploader {
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        background-color: #161b22;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }
    /* تصميم الأزرار */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00f2ff, #7000ff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px;
        font-size: 1.2rem;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px #00f2ff;
        color: white;
    }
    /* رسائل النجاح والخطأ */
    .stAlert {
        border-radius: 12px;
        background-color: #161b22;
        border: 1px solid #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚀 نظام الإكسيل - يوسف باشا</p>', unsafe_allow_html=True)

# المربع الرئيسي لرفع الملف
with st.container():
    uploaded_file = st.file_uploader("ارفع ملف الإكسيل هنا", type=["xlsx"])

def force_to_time(val):
    """تحويل القيمة لوقت مهما كان نوعها (حتى لو نتيجة معادلة)"""
    if isinstance(val, (time, datetime)):
        return val if isinstance(val, time) else val.time()
    if isinstance(val, str):
        val = val.strip()
        for fmt in ["%H:%M", "%I:%M %p", "%H:%M:%S"]:
            try: return datetime.strptime(val, fmt).time()
            except: continue
    return None

if uploaded_file is not None:
    st.info("📦 تم استلام الملف بنجاح، جاهز للاختراق!")
    if st.button("تعديل كافة السجلات المفتوحة (9 ساعات)"):
        with st.spinner('جاري فحص البيانات وتعديل الساعات...'):
            # قراءة البيانات مع المعادلات
            wb = openpyxl.load_workbook(uploaded_file, data_only=True)
            sheet = wb.active
            
            # نسخة الكتابة
            wb_write = openpyxl.load_workbook(uploaded_file)
            sheet_write = wb_write.active
            
            updates = 0
            no_fill = PatternFill(fill_type=None)

            for r in range(1, sheet.max_row + 1):
                c_val = sheet.cell(row=r, column=3).value # الحضور
                d_val = sheet.cell(row=r, column=4).value # الانصراف
                
                t_in = force_to_time(c_val)
                
                if t_in and (d_val is None or str(d_val).strip() in ["", "0", "00:00:00", "None"]):
                    dt_in = datetime.combine(datetime.today(), t_in)
                    dt_out = dt_in + timedelta(hours=9)
                    
                    target_d = sheet_write.cell(row=r, column=4)
                    target_g = sheet_write.cell(row=r, column=7)
                    
                    target_d.value = dt_out.strftime('%H:%M')
                    target_g.value = 9.0
                    
                    # تنظيف التنسيق
                    target_d.fill = no_fill
                    sheet_write.cell(row=r, column=3).fill = no_fill
                    
                    updates += 1

            output = io.BytesIO()
            wb_write.save(output)
            
            if updates > 0:
                st.balloons() # احتفال بالنجاح
                st.success(f"✅ تم تعديل {updates} سطر بنجاح يا باشا!")
                st.download_button(
                    label="📥 تحميل الملف المعدل الآن",
                    data=output.getvalue(),
                    file_name="Youssef_Final_9Hours.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("البرنامج مش شايف خانات ناقصة. اتأكد إن الحضور في عمود C والانصراف في D.")