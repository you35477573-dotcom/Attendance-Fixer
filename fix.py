import streamlit as st
import openpyxl
from openpyxl.styles import PatternFill
from datetime import datetime, timedelta, time
import io

st.set_page_config(page_title="Youssef Pasha - The Ultimate Fix", layout="wide")
st.title("🚀 النظام النهائي لقهر الإكسيل - يوسف باشا")

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
    if st.button("تعديل كافة السجلات المفتوحة (9 ساعات)"):
        with st.spinner('جاري اختراق المعادلات وتعديل الساعات...'):
            # ميزة data_only=True هي السر؛ بتقرأ الأرقام مش المعادلات
            wb = openpyxl.load_workbook(uploaded_file, data_only=True)
            sheet = wb.active
            
            # بنفتح نسخة تانية عشان نكتب فيها (للحفاظ على المعادلات الأصلية)
            wb_write = openpyxl.load_workbook(uploaded_file)
            sheet_write = wb_write.active
            
            updates = 0
            no_fill = PatternFill(fill_type=None)

            # المسح الشامل من الصف 1 لحد 1000 مثلاً
            for r in range(1, sheet.max_row + 1):
                # بنقرأ من نسخة الـ data_only (الأرقام الحقيقية)
                c_val = sheet.cell(row=r, column=3).value # الحضور
                d_val = sheet.cell(row=r, column=4).value # الانصراف
                
                t_in = force_to_time(c_val)
                
                # لو فيه حضور ومافيش انصراف (أو الانصراف صفر)
                if t_in and (d_val is None or str(d_val).strip() in ["", "0", "00:00:00", "None"]):
                    # حساب الـ 9 ساعات
                    dt_in = datetime.combine(datetime.today(), t_in)
                    dt_out = dt_in + timedelta(hours=9)
                    
                    # الكتابة في نسخة الـ Write (اللي هنحملها)
                    target_d = sheet_write.cell(row=r, column=4)
                    target_g = sheet_write.cell(row=r, column=7)
                    
                    target_d.value = dt_out.strftime('%H:%M')
                    target_g.value = 9.0
                    
                    # تنظيف اللون الأصفر
                    target_d.fill = no_fill
                    sheet_write.cell(row=r, column=3).fill = no_fill
                    
                    updates += 1

            output = io.BytesIO()
            wb_write.save(output)
            
            if updates > 0:
                st.success(f"✅ مبروك يا باشا! تم تعديل {updates} سطر بنجاح.")
                st.download_button("📥 تحميل الملف المعدل الآن", data=output.getvalue(), file_name="Youssef_Final_9Hours.xlsx")
            else:
                st.error("البرنامج لسه مش شايف الخلايا. جرب تتأكد إن الحضور في العمود رقم 3 (C).")