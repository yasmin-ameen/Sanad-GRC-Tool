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

policy_df = pd.DataFrame({
    "اسم السياسة": ["سياسة أمن المعلومات", "سياسة الخصوصية", "سياسة إدارة الأصول"],
    "الإصدار": ["v2.1", "v1.0", "v1.5"],
    "حالة الاعتماد": ["معتمدة", "معتمدة", "قيد المراجعة"],
})

# ============================================================
# Navigation (names defined once so menu and conditions always match)
# ============================================================
DASHBOARD = "لوحة المؤشرات"
RISKS = "سجل المخاطر المؤسسية"
COMPLIANCE = "الالتزام والسياسات"

menu = st.sidebar.selectbox("اختر القسم:", [DASHBOARD, RISKS, COMPLIANCE])

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

elif menu == COMPLIANCE:
    st.header("📜 الالتزام والسياسات")
    st.write("متابعة متطلبات الحوكمة والالتزام المؤسسي وضمان تطبيق المعايير.")
    st.table(policy_df)
