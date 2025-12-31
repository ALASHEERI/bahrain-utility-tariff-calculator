import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ---------------------------
# إعداد الصفحة
# ---------------------------
st.set_page_config(page_title="Bahrain Utility Tariff Calculator", layout="centered")

# ---------------------------
# اختيار اللغة
# ---------------------------
lang = st.selectbox("Language / اللغة", ["English", "العربية"])

texts = {
    "ar": {
        "title": "حاسبة التعرفة الكهربائية، المائية والبترولية – البحرين",
        "electricity": "⚡ التعرفة الكهربائية للمنزل",
        "water": "💧 التعرفة المائية للمنزل",
        "fuel": "⛽ تعرفة الوقود",
        "results": "📊 النتائج",
        "old_bill": "الفاتورة السابقة",
        "new_bill": "الفاتورة الجديدة",
        "difference": "الفرق",
        "increase": "نسبة الزيادة %",
        "kwh_used": "عدد الوحدات المستخدمة",
        "m3_used": "عدد المتر المكعب المستخدم",
        "liters_used": "عدد اللترات المستخدمة",
        "done_by": "Done by: Eng. Mohamed Jaber ALASHEERI",
        "share_text": "📤 شارك الحاسبة مع الآخرين",
        "share_info": "يمكنك مشاركة الرابط التالي مع الآخرين:",
        "units": {"electricity":"kWh","water":"m³","fuel":"liters","currency":"BHD"}
    },
    "en": {
        "title": "Bahrain Utility Tariff Calculator",
        "electricity": "⚡ EWA Residential Electricity Tariff",
        "water": "💧 EWA Residential Water Tariff",
        "fuel": "⛽ Fuel Tariff",
        "results": "📊 Results",
        "old_bill": "Previous bill",
        "new_bill": "Current bill",
        "difference": "Difference",
        "increase": "Increase %",
        "kwh_used": "Units consumed",
        "m3_used": "Cubic meters used",
        "liters_used": "Liters used",
        "done_by": "Done by: Eng. Mohamed Jaber ALASHEERI",
        "share_text": "📤 Share the calculator with others",
        "share_info": "You can share the following link with others:",
        "units": {"electricity":"kWh","water":"m³","fuel":"liters","currency":"BHD"}
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
    bill_input = st.number_input("Enter previous bill / أدخل قيمة الفاتورة السابقة (BHD / د.ب)", min_value=0.0, step=0.01, format="%.2f", key="elec_bill")
    usage_input = st.number_input("Enter consumption / أدخل الاستهلاك (kWh)", min_value=0.0, step=1.0, format="%.1f", key="elec_usage")

    slabs = [
        (3000, 0.003, 0.003),
        (2000, 0.009, 0.009),
        (float("inf"), 0.016, 0.032)
    ]
    slab_names_ar = ["الشريحة الأولى","الشريحة الثانية","الشريحة الثالثة"]
    slab_names_en = ["First slab","Second slab","Third slab"]
    colors = ["#27ae60","#f1c40f","#e74c3c"]

    # حساب الوحدات لو المستخدم أدخل الفاتورة فقط
    if bill_input>0 and usage_input==0:
        remaining = bill_input
        usage = 0
        for limit, old_price, _ in slabs:
            max_cost = limit*old_price
            if remaining > max_cost:
                usage += limit
                remaining -= max_cost
            else:
                usage += remaining/old_price
                break
    else:
        usage = usage_input

    usage_list = [0,0,0]
    remaining = usage
    for i,(limit,_,_) in enumerate(slabs):
        if remaining>limit:
            usage_list[i]=limit
            remaining-=limit
        else:
            usage_list[i]=remaining
            remaining=0
            break

    old_cost = sum(u*s[1] for u,s in zip(usage_list, slabs))
    new_cost = sum(u*s[2] for u,s in zip(usage_list, slabs))
    diff = new_cost - old_cost
    percent = (diff/old_cost*100) if old_cost>0 else 0

    st.subheader(t["results"])
    st.metric(t["old_bill"], f"{old_cost:.3f} {t['units']['currency']}")
    st.metric(t["new_bill"], f"{new_cost:.3f} {t['units']['currency']}")
    st.metric(t["difference"], f"{diff:.3f} {t['units']['currency']}", f"{percent:.1f}%")
    st.info(f"{t['kwh_used']}: {sum(usage_list):.1f} {t['units']['electricity']}")

    labels = slab_names_ar if lang=="العربية" else slab_names_en
    fig = go.Figure()
    for i in range(3):
        fig.add_trace(go.Bar(
            y=["Usage" if lang=="English" else "الاستهلاك"],
            x=[usage_list[i]],
            name=labels[i],
            orientation="h",
            marker=dict(color=colors[i], line=dict(color='black', width=1)),
            hovertemplate=f"%{{x:.3f}} {t['units']['electricity']}<br>%{{fullData.name}}"
        ))
    fig.update_layout(
        barmode='stack',
        height=300,
        xaxis_title=t['units']['electricity'],
        yaxis_visible=False,
        legend_title_text="Slab" if lang=="English" else "الشريحة"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 💧 الماء
# ---------------------------
with tab2:
    bill_input = st.number_input("Enter previous bill / أدخل قيمة الفاتورة السابقة (BHD / د.ب)", min_value=0.0, step=0.01, format="%.2f", key="water_bill")
    usage_input = st.number_input("Enter consumption / أدخل الاستهلاك (m³ / م³)", min_value=0.0, step=1.0, format="%.1f", key="water_usage")

    slabs = [
        (60, 0.025,0.025),
        (40, 0.08,0.08),
        (float("inf"), 0.2,0.775)
    ]
    slab_names_ar = ["الشريحة الأولى","الشريحة الثانية","الشريحة الثالثة"]
    slab_names_en = ["First slab","Second slab","Third slab"]
    colors = ["#3498db","#f1c40f","#e74c3c"]

    if bill_input>0 and usage_input==0:
        remaining = bill_input
        usage = 0
        for limit, old_price, _ in slabs:
            max_cost = limit*old_price
            if remaining>max_cost:
                usage += limit
                remaining -= max_cost
            else:
                usage += remaining/old_price
                break
    else:
        usage = usage_input

    usage_list = [0,0,0]
    remaining = usage
    for i,(limit,_,_) in enumerate(slabs):
        if remaining>limit:
            usage_list[i]=limit
            remaining-=limit
        else:
            usage_list[i]=remaining
            remaining=0
            break

    old_cost = sum(u*s[1] for u,s in zip(usage_list, slabs))
    new_cost = sum(u*s[2] for u,s in zip(usage_list, slabs))
    diff = new_cost - old_cost
    percent = (diff/old_cost*100) if old_cost>0 else 0

    st.subheader(t["results"])
    st.metric(t["old_bill"], f"{old_cost:.3f} {t['units']['currency']}")
    st.metric(t["new_bill"], f"{new_cost:.3f} {t['units']['currency']}")
    st.metric(t["difference"], f"{diff:.3f} {t['units']['currency']}", f"{percent:.1f}%")
    st.info(f"{t['m3_used']}: {sum(usage_list):.1f} {t['units']['water']}")

    labels = slab_names_ar if lang=="العربية" else slab_names_en
    fig = go.Figure()
    for i in range(3):
        fig.add_trace(go.Bar(
            y=["Usage" if lang=="English" else "الاستهلاك"],
            x=[usage_list[i]],
            name=labels[i],
            orientation="h",
            marker=dict(color=colors[i], line=dict(color='black', width=1)),
            hovertemplate=f"%{{x:.3f}} {t['units']['water']}<br>%{{fullData.name}}"
        ))
    fig.update_layout(
        barmode='stack',
        height=300,
        xaxis_title=t['units']['water'],
        yaxis_visible=False,
        legend_title_text="Slab" if lang=="English" else "الشريحة"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# ⛽ البترول
# ---------------------------
with tab3:
    fuel_prices = pd.DataFrame({
        "fuel":["جيد 91","ممتاز 95","سوبر 98","ديزل"],
        "old_price":[0.14,0.20,0.235,0.18],
        "new_price":[0.22,0.235,0.265,0.2]
    })
    total_old = 0
    total_new = 0
    total_liters = 0

    for index, row in fuel_prices.iterrows():
        liters = st.number_input(f"{row['fuel']} – عدد اللترات (liters / لتر)", min_value=0.0, step=0.001, format="%.3f")
        total_liters += liters
        total_old += liters*row['old_price']
        total_new += liters*row['new_price']

    if total_old>0:
        diff = total_new - total_old
        percent = (diff/total_old*100)
        st.subheader(t["results"])
        st.metric(t["old_bill"], f"{total_old:.3f} {t['units']['currency']}")
        st.metric(t["new_bill"], f"{total_new:.3f} {t['units']['currency']}")
        st.metric(t["difference"], f"{diff:.3f} {t['units']['currency']}", f"{percent:.1f}%")
        st.info(f"{t['liters_used']}: {total_liters:.3f} {t['units']['fuel']}")

# ---------------------------
# زر نشر الحاسبة بدون أي حساب
# ---------------------------
st.markdown("---")
st.markdown(f"### {t['share_text']}")
app_url = "https://bahrain-utility-tariff-calculator-bnlwpywuk8lkbqfuunw8gl.streamlit.app/"  # ضع هنا رابط الصفحة من المتصفح
if st.button("🔗 Open / افتح الحاسبة"):
    st.write(f"{t['share_info']} {app_url}")


st.caption(t["done_by"])
