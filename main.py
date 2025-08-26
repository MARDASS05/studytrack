import streamlit as st
import datetime
import json

# ---- Ayarlar ----
st.set_page_config(page_title="StudyTrack", page_icon="📘", layout="centered")

# ---- Tema Seçimi ----
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

theme = st.sidebar.radio("🌙 Tema Seç", ["light", "dark"])
st.session_state["theme"] = theme

bg_color = "#FFFFFF" if theme == "light" else "#1C1C1E"
text_color = "#000000" if theme == "light" else "#FFFFFF"
accent_color = "#007AFF"

st.markdown(
    f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Görev Verileri ----
if "tasks" not in st.session_state:
    st.session_state["tasks"] = {}

today = str(datetime.date.today())

if today not in st.session_state["tasks"]:
    st.session_state["tasks"][today] = []

# ---- Ana Sayfa ----
st.title("📘 StudyTrack")
st.write(f"📅 Bugün: {today}")

# Görev ekleme
new_task = st.text_input("Yeni görev ekle (örn: Matematik - Limit)")
if st.button("➕ Ekle") and new_task:
    st.session_state["tasks"][today].append({"text": new_task, "done": False})

# Görev listesi
if st.session_state["tasks"][today]:
    st.subheader("Bugünün Görevleri")
    for i, task in enumerate(st.session_state["tasks"][today]):
        done = st.checkbox(task["text"], value=task["done"], key=f"{today}_{i}")
        st.session_state["tasks"][today][i]["done"] = done
else:
    st.info("Bugün için görev eklemedin.")

# ---- İstatistik ----
st.subheader("📊 İstatistikler")

# Günlük istatistik
today_done = sum(1 for t in st.session_state["tasks"][today] if t["done"])
today_total = len(st.session_state["tasks"][today])
st.write(f"✔ Bugün: {today_done}/{today_total} görev tamamlandı")

# Genel istatistik
all_done = sum(1 for d in st.session_state["tasks"].values() for t in d if t["done"])
all_total = sum(len(d) for d in st.session_state["tasks"].values())
progress = int(all_done / all_total * 100) if all_total > 0 else 0
st.progress(progress/100)
st.write(f"📈 Genel ilerleme: %{progress}")

# ---- Haftalık Grafik ----
import matplotlib.pyplot as plt

days = []
values = []
for i in range(6,-1,-1):
    day = str(datetime.date.today() - datetime.timedelta(days=i))
    done = sum(1 for t in st.session_state["tasks"].get(day, []) if t["done"])
    days.append(day[5:])  # ay-gün
    values.append(done)

fig, ax = plt.subplots(figsize=(6,2))
ax.plot(days, values, color=accent_color, linewidth=2, marker="o")
ax.set_title("Son 7 Günlük Çalışma")
ax.set_ylabel("Görev")
st.pyplot(fig)
