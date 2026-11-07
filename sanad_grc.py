import streamlit as st
import pandas as pd

# ============================================================
# Page settings
# ============================================================
st.set_page_config(
    page_title="منظومة سند GRC",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ منظومة سند GRC - إدارة المخاطر والالتزام")
st.caption("⚠️ البيانات المعروضة تجريبية لأغراض العرض والتعلم.")
st.markdown("---")

# ============================================================
# Sample data (single source of truth for all sections)
# ============================================================
risk_df = pd.DataFrame({
    "رقم المخاطر": ["RSK-001", "RSK-002", "RSK-003", "RSK-004"],
    "وصف المخاطر": [
        "انقطاع الخدمات السحابية الأساسية",
        "تسريب بيانات العملاء الحساسة",
        "عدم الالتزام بالمتطلبات التنظيمية للجهات الرقابية",
        "فشل استمرارية الأعمال في الموقع الرئيسي",
    ],
    "مستوى الخطر": ["عالي", "عالي", "متوسط", "منخفض"],
    "الإدارة المعنية": ["تقنية المعلومات", "أمن المعلومات", "الشؤون القانونية", "العمليات"],
    "الحالة": ["قيد المعالجة", "مفتوحة", "مفتوحة", "مغلقة"],
})

# Each risk is linked to a control AND the evidence that proves it.
# NOTE: control numbers are examples; verify them against the official
# NCA ECC-2:2024 document before using them in a real assessment.
controls_df = pd.DataFrame({
    "رقم المخاطر": ["RSK-001", "RSK-002", "RSK-003", "RSK-004"],
    "الضابط (NCA ECC)": ["ECC 4-2", "ECC 2-7", "ECC 1-7", "ECC 3-1"],
    "الدليل": [
        "تقرير توفر الخدمة السحابية الشهري",
        "سجل صلاحيات الوصول إلى بيانات العملاء",
        "تقرير مراجعة الالتزام التنظيمي",
        "خطة استمرارية الأعمال ونتيجة تمرين المحاكاة",
    ],
    "مالك الدليل": ["مدير تقنية المعلومات", "مدير أمن المعلومات", "مسؤول الالتزام", "مدير العمليات"],
    "تاريخ آخر اختبار": pd.to_datetime(["2026-08-20", "2026-03-10", None, "2026-10-01"]),
    "نتيجة الاختبار": ["ناجح", "فاشل", "لم يُختبر", "ناجح"],
})

policy_df = pd.DataFrame({
    "اسم السياسة": ["سياسة أمن المعلومات", "سياسة الخصوصية", "سياسة إدارة الأصول"],
    "الإصدار": ["v2.1", "v1.0", "v1.5"],
    "حالة الاعتماد": ["معتمدة", "معتمدة", "قيد المراجعة"],
})

STALE_DAYS = 180  # a test older than this is considered overdue

# ============================================================
# Navigation (names defined once so menu and conditions always match)
# ============================================================
DASHBOARD = "لوحة المؤشرات"
RISKS = "سجل المخاطر المؤسسية"
CONTROLS = "الضوابط والأدلة"
COMPLIANCE = "الالتزام والسياسات"

menu = st.sidebar.selectbox("اختر القسم:", [DASHBOARD, RISKS, CONTROLS, COMPLIANCE])

# ============================================================
# Sections
# ============================================================
if menu == DASHBOARD:
    st.header("📊 لوحة المؤشرات الرئيسية")

    total_risks = len(risk_df)
    high_risks = int((risk_df["مستوى الخطر"] == "عالي").sum())
    open_risks = int((risk_df["الحالة"] != "مغلقة").sum())
    approved = int((policy_df["حالة الاعتماد"] == "معتمدة").sum())
    approval_rate = round(approved / len(policy_df) * 100)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي المخاطر المسجلة", total_risks)
    col2.metric("المخاطر المرتفعة", high_risks)
    col3.metric("المخاطر غير المغلقة", open_risks)
    col4.metric("السياسات المعتمدة", f"{approval_rate}%")

    # Evidence metrics (calculated from the controls table)
    today = pd.Timestamp.today().normalize()
    days_since_test = (today - controls_df["تاريخ آخر اختبار"]).dt.days
    untested = int(controls_df["تاريخ آخر اختبار"].isna().sum())
    overdue = int((days_since_test > STALE_DAYS).sum())
    failed = int((controls_df["نتيجة الاختبار"] == "فاشل").sum())

    col5, col6, col7 = st.columns(3)
    col5.metric("ضوابط لم تُختبر", untested)
    col6.metric(f"اختبارات متأخرة (+{STALE_DAYS} يوم)", overdue)
    col7.metric("ضوابط فاشلة", failed)

    st.markdown("---")
    st.subheader("توزيع المخاطر حسب المستوى")
    st.bar_chart(risk_df["مستوى الخطر"].value_counts())

elif menu == RISKS:
    st.header("📋 سجل المخاطر المؤسسية")

    levels = st.multiselect(
        "تصفية حسب مستوى الخطر:",
        options=["عالي", "متوسط", "منخفض"],
        default=["عالي", "متوسط", "منخفض"],
    )
    st.dataframe(risk_df[risk_df["مستوى الخطر"].isin(levels)])

elif menu == CONTROLS:
    st.header("🔗 الضوابط والأدلة")
    st.write("ربط كل خطر بالضابط الذي يعالجه وبالدليل الذي يثبت تطبيقه.")

    view = controls_df.copy()
    view.insert(
        1, "وصف المخاطر",
        view["رقم المخاطر"].map(risk_df.set_index("رقم المخاطر")["وصف المخاطر"]),
    )
    view["تاريخ آخر اختبار"] = (
        view["تاريخ آخر اختبار"].dt.strftime("%Y-%m-%d").fillna("لم يُختبر")
    )
    st.dataframe(view)

elif menu == COMPLIANCE:
    st.header("📜 الالتزام والسياسات")
    st.write("متابعة متطلبات الحوكمة والالتزام المؤسسي وضمان تطبيق المعايير.")
    st.table(policy_df)
