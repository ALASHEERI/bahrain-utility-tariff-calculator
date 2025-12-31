import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ---------------------------
# إعداد الصفحة
# ---------------------------
st.set_page_config(page_title="Bahrain Utility Tariff Calculator", layout="centered")

# اختيار اللغة
lang = st.selectbox("Language / اللغة", ["English", "العربية"])

texts = {
    "ar": {
        "title": "حاسبة التعرفة الكهربائية، المائية والبترولية – البحرين",
        "electricity": "⚡ التعرفة الكهربائية للمنزل",
        "water": "💧 التعرفة المائية للمنزل",
        "fuel": "⛽ تعرفة الوقود",
        "enter_bill": "أدخل قيمة الفاتورة (د.ب)",
        "enter_usage": "أدخل الاستهلاك",
        "results": "📊 النتائج",
        "old_bill": "الفاتورة السابقة (د.ب)",
        "new_bill": "الفاتورة الجديدة (د.ب)",
        "difference": "الفرق (د.ب)",
        "increase": "نسبة الزيادة %",
        "kwh_used": "عدد الوحدات المستخدمة (kWh)",
        "m3_used": "عدد المتر المكعب المستخدم (م³)",
        "liters_used": "عدد اللترات المستخدمة",
        "done_by": "Done by: Eng. Mohamed Jaber ALASHEERI",
        "share_text": "📤 شارك الحاسبة مع الآخرين",
        "share_button": "📤 نشر الحاسبة",
        "share_info": "يمكنك مشاركة الرابط التالي مع الآخرين:"
    },
    "en": {
        "title": "Bahrain Utility Tariff Calculator",
        "electricity": "⚡ EWA Residential Electricity Tariff",
        "water": "💧 EWA Residential Water Tariff",
        "fuel": "⛽ Fuel Tariff",
        "enter_bill": "Enter bill amount (BHD)",
        "enter_usage": "Enter usage",
        "results": "📊 Results",
        "old_bill": "Previous bill (BHD)",
        "new_bill": "Current bill (BHD)",
        "difference": "Difference (BHD)",
        "increase": "Increase %",
        "kwh_used": "Units consumed (kWh)",
        "m3_used": "Cubic meters used (m³)",
        "liters_used": "Liters used",
        "done_by": "Done by: Eng. Mohamed Jaber ALASHEERI",
        "share_text": "📤 Share the calculator with others",
        "share_button": "📤 Publish Calculator",
        "share_info": "You can share the following link with others:"
    }
}

t = texts["ar"] if lang=="العربية" else texts["en"]

st.title(t["title"])

# ---------------------------
# Tabs للكهرباء والماء والبترول
# ---------------------------
tab1, tab2, tab3 = st.tabs([t["electricity"], t["water"], t["fuel"]])

# ---------------------------
# ⚡ الكهرباء
# ---------------------------
with tab1:
    input_type = st.radio(t["enter_bill"], [t["enter_bill"], t["enter_usage"]], horizontal=True, key="elec_input_type")
    value = st.number_input("", min_value=0.0, step=1.0, key="elec_value")

    slabs = [
        (3000, 0.003, 0.003),
        (2000, 0.009, 0.009),
        (float("inf"), 0.016, 0.032)
    ]
    slab_names_ar = ["الشريحة الأولى","الشريحة الثانية","الشريحة الثالثة"]
    slab_names_en = ["First slab","Second slab","Third slab"]
    colors = ["#27ae60","#f1c40f","#e74c3c"]

    def calc_usage(bill, slabs):
        remaining = bill
        usage=[]
        for limit, price_old, _ in slabs:
            max_cost = limit*price_old
            if remaining>=max_cost:
                usage.append(limit)
                remaining-=max_cost
            else:
                usage.append(remaining/price_old if price_old else 0)
                remaining=0
                break
        while len(usage)<3:
            usage.append(0)
        return usage

    if value>0:
        if input_type==t["enter_bill"]:
            usage = calc_usage(value, slabs)
        else:
            remaining=value
            usage=[]
            for limit,_,_ in slabs:
                if remaining>limit:
                    usage.append(limit)
                    remaining-=limit
                else:
                    usage.append(remaining)
                    remaining=0
                    break
            while len(usage)<3:
                usage.append(0)

        old_cost = sum(u*s[1] for u,s in zip(usage, slabs))
        new_cost = sum(u*s[2] for u,s in zip(usage, slabs))
        diff = new_cost - old_cost
        percent = (diff/old_cost*100) if old_cost>0 else 0

        st.subheader(t["results"])
        c1,c2 = st.columns(2)
        c1.metric(t["old_bill"], f"{old_cost:.2f} د.ب")
        c2.metric(t["new_bill"], f"{new_cost:.2f} د.ب")
        st.metric(t["difference"], f"{diff:.2f} د.ب", f"{percent:.1f}%")

        if input_type==t["enter_bill"]:
            st.info(f"{t['kwh_used']}: {sum(usage):.1f}")

        # ---------------------------
        # Visuals جذابة
        # ---------------------------
        labels = slab_names_ar if lang=="العربية" else slab_names_en
        fig = go.Figure()
        for i in range(3):
            fig.add_trace(go.Bar(
                y=["الاستهلاك" if lang=="العربية" else "Usage"],
                x=[usage[i]],
                name=labels[i],
                orientation="h",
                marker=dict(color=colors[i], line=dict(color='black', width=1))
            ))
        fig.update_layout(
            barmode='stack',
            height=300,
            xaxis_title="kWh",
            yaxis_visible=False,
            legend_title_text="الشريحة" if lang=="العربية" else "Slab"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 💧 الماء
# ---------------------------
with tab2:
    input_type = st.radio(t["enter_bill"], [t["enter_bill"], t["enter_usage"]], horizontal=True, key="water_input_type")
    value = st.number_input("", min_value=0.0, step=1.0, key="water_value")

    slabs = [
        (60, 0.025,0.025),
        (40, 0.08,0.08),
        (float("inf"), 0.2,0.775)
    ]
    slab_names_ar = ["الشريحة الأولى","الشريحة الثانية","الشريحة الثالثة"]
    slab_names_en = ["First slab","Second slab","Third slab"]
    colors = ["#3498db","#f1c40f","#e74c3c"]

    def calc_usage_water(bill, slabs):
        remaining = bill
        usage=[]
        for limit, price_old,_ in slabs:
            max_cost = limit*price_old
            if remaining>=max_cost:
                usage.append(limit)
                remaining-=max_cost
            else:
                usage.append(remaining/price_old if price_old else 0)
                remaining=0
                break
        while len(usage)<3:
            usage.append(0)
        return usage

    if value>0:
        if input_type==t["enter_bill"]:
            usage = calc_usage_water(value, slabs)
        else:
            remaining=value
            usage=[]
            for limit,_,_ in slabs:
                if remaining>limit:
                    usage.append(limit)
                    remaining-=limit
                else:
                    usage.append(remaining)
                    remaining=0
                    break
            while len(usage)<3:
                usage.append(0)

        old_cost = sum(u*s[1] for u,s in zip(usage, slabs))
        new_cost = sum(u*s[2] for u,s in zip(usage, slabs))
        diff = new_cost - old_cost
        percent = (diff/old_cost*100) if old_cost>0 else 0

        st.subheader(t["results"])
        c1,c2 = st.columns(2)
        c1.metric(t["old_bill"], f"{old_cost:.2f} د.ب")
        c2.metric(t["new_bill"], f"{new_cost:.2f} د.ب")
        st.metric(t["difference"], f"{diff:.2f} د.ب", f"{percent:.1f}%")

        if input_type==t["enter_bill"]:
            st.info(f"{t['m3_used']}: {sum(usage):.1f}")

        # ---------------------------
        # Visuals جذابة
        # ---------------------------
        labels = slab_names_ar if lang=="العربية" else slab_names_en
        fig = go.Figure()
        for i in range(3):
            fig.add_trace(go.Bar(
                y=["الاستهلاك" if lang=="العربية" else "Usage"],
                x=[usage[i]],
                name=labels[i],
                orientation="h",
                marker=dict(color=colors[i], line=dict(color='black', width=1))
            ))
        fig.update_layout(
            barmode='stack',
            height=300,
            xaxis_title="م³",
            yaxis_visible=False,
            legend_title_text="الشريحة" if lang=="العربية" else "Slab"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# ⛽ البترول
# ---------------------------
with tab3:
    fuel_prices = pd.read_csv("fuel_prices.csv")
    total_old = 0
    total_new = 0
    total_liters = 0

    for index, row in fuel_prices.iterrows():
        liters = st.number_input(f"{row['fuel']} – عدد اللترات (لتر)", min_value=0.0, step=1.0, key=f"fuel_{index}")
        total_liters += liters
        total_old += liters*row['old_price']
        total_new += liters*row['new_price']

    if total_old>0:
        diff = total_new - total_old
        percent = (diff/total_old*100)
        st.subheader(t["results"])
        st.metric(t["old_bill"], f"{total_old:.2f} د.ب")
        st.metric(t["new_bill"], f"{total_new:.2f} د.ب")
        st.metric(t["difference"], f"{diff:.2f} د.ب", f"{percent:.1f}%")
        st.info(f"{t['liters_used']}: {total_liters:.1f}")

# ---------------------------
# زر نشر الحاسبة
# ---------------------------
st.markdown("---")
st.markdown(f"### {t['share_text']}")
app_url = "https://bahrain-utility-tariff-calculator.streamlit.app"
if st.button(t["share_button"]):
    st.info(f"{t['share_info']} [الرابط]({app_url})")

# ---------------------------
# اسمك في الأسفل
# ---------------------------
st.markdown("---")
st.caption(t["done_by"])

