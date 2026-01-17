import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Smart Waste AI", layout="wide")

st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}

.stApp {
    background: linear-gradient(120deg,#ecfeff,#d1fae5);
}

.title {
    font-size: 48px;
    font-weight: 800;
    color: #064e3b;
}
.subtitle {
    color: #065f46;
    font-size: 18px;
    margin-bottom: 30px;
}

[data-testid="stVerticalBlock"] > div:has(> [data-testid="column"]) {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 0 40px rgba(0,0,0,0.1);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("waste_classifier_mobilenet.h5")

@st.cache_data
def load_companies():
    return pd.read_excel("companies.xlsx")

model = load_model()
companies_df = load_companies()

class_names = [
    "battery","biological","cardboard","clothes","glass",
    "metal","paper","plastic","shoes","trash"
]

waste_rules = {
    "battery": {"type":"Hazardous","message":"⚠ Battery waste is dangerous.","action":"Send to hazardous waste unit"},
    "biological": {"type":"Organic","message":"🌱 Biodegradable waste detected.","action":"Send to compost"},
    "plastic": {"type":"Recyclable","message":"♻ Plastic can be recycled.","action":"Send to plastic recycling"},
    "glass": {"type":"Recyclable","message":"♻ Glass can be recycled.","action":"Send to glass recycling"},
    "metal": {"type":"Recovery","message":"💰 Metal has recovery value.","action":"Send for metal recovery"},
    "paper": {"type":"Recyclable","message":"📄 Paper detected.","action":"Send to paper recycling"},
    "cardboard": {"type":"Recyclable","message":"📦 Cardboard detected.","action":"Send to cardboard recycling"},
    "clothes": {"type":"Recovery","message":"👕 Clothes can be reused.","action":"Send to donation / recovery center"},
    "shoes": {"type":"Landfill","message":"👟 Shoes are not recyclable.","action":"Send to landfill"},
    "trash": {"type":"Landfill","message":"🗑 General waste.","action":"Dispose safely"}
}

if "stats" not in st.session_state:
    st.session_state.stats = {"total":0,"recyclable":0,"hazardous":0,"recovered":0}

st.markdown("## 🌍 Smart City Waste Monitor")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Waste", st.session_state.stats["total"])
c2.metric("Recyclable", st.session_state.stats["recyclable"])
c3.metric("Hazardous", st.session_state.stats["hazardous"])
c4.metric("Recovered", st.session_state.stats["recovered"])

st.markdown("<div class='title'>♻ Smart Waste AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered waste classification for Smart Cities</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Upload Waste Image")
    uploaded = st.file_uploader("", type=["jpg","png","jpeg"])

with col2:
    st.subheader("🧠 AI Prediction")

    if uploaded:
        if "last_file" not in st.session_state or st.session_state.last_file != uploaded.name:
            img = Image.open(uploaded).convert("RGB")
            img_resized = img.resize((224,224))
            arr = np.expand_dims(np.array(img_resized)/255.0, axis=0)

            with st.spinner("AI scanning waste..."):
                pred = model.predict(arr)

            idx = np.argmax(pred)
            confidence = float(np.max(pred)*100)
            label = class_names[idx]

            st.session_state.last_file = uploaded.name
            st.session_state.result = (img, label, confidence)

            st.session_state.stats["total"] += 1
            if waste_rules[label]["type"] == "Hazardous":
                st.session_state.stats["hazardous"] += 1
            elif waste_rules[label]["type"] in ["Recyclable","Organic"]:
                st.session_state.stats["recyclable"] += 1
            elif waste_rules[label]["type"] == "Recovery":
                st.session_state.stats["recovered"] += 1
        else:
            img, label, confidence = st.session_state.result

        rule = waste_rules[label]
        st.image(img, width=250)
        st.success(f"**{label.upper()}** ({confidence:.2f}%)")
        st.info(rule["message"])
        st.warning(f"Action: {rule['action']}")

        matches = companies_df[companies_df["Waste_Needed"] == label]

        if not matches.empty:
            st.markdown("### 🏭 Suggested Recycling / Recovery Companies")
            for _, row in matches.iterrows():
                st.markdown(
                    f"**{row['Company_Names']}**  \n"
                    f"📍 {row['Location']}  \n"
                    f"🌐 [{row['Website']}]({row['Website']})"
                )
        else:
            st.info("No registered companies available for this waste type.")

    else:
        st.info("Upload an image to get AI result")
