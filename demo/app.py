import dis
import streamlit as st
import requests
import os
import time


st.set_page_config(page_title="AI Clarity Companion",
                   page_icon="✨", layout="wide")


def typewriter_effect(text, label="Coach:", delay=0.02):
    """Display text one character at a time like a typewriter."""
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.text_area(label, value=displayed,
                              height=220, disabled=True)
        time.sleep(delay)
    return displayed


st.title("✨ AI Clarity Companion (Portfolio App)")

# Basic config
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

# Sidebar
st.sidebar.header("Demo Settings")
user_id = st.sidebar.text_input("User ID", value="demo_user")
st.sidebar.markdown("Backend must be running at **localhost:8000**")

# Columns
c1, c2 = st.columns(2)

with c1:
    st.subheader("Chat")

    # input + send button on top
    msg = st.text_input(
        "What's on your mind:",
        value="",
        placeholder="Talk to your AI Coach here..."
    )

    colA, colB = st.columns([1, 5])
    with colA:
        send_clicked = st.button("Ask", use_container_width=True)
    with colB:
        st.write("")  # spacer

    # keep coach reply in session so it persists across reruns
    if "coach_reply" not in st.session_state:
        st.session_state.coach_reply = ""
    if "coach_context_used" not in st.session_state:
        st.session_state.coach_context_used = False
    if "coach_recall" not in st.session_state:
        st.session_state.coach_recall = []

    if send_clicked:
        try:
            r = requests.post(
                f"{API_BASE}/chat",
                json={"user_id": user_id, "message": msg},
                timeout=180
            )
            data = r.json()
            st.session_state.coach_reply = (data.get("reply") or "").strip()
            st.session_state.coach_context_used = bool(
                data.get("context_used"))
            st.session_state.coach_recall = data.get("recall") or []
        except Exception as e:
            st.session_state.coach_reply = f"(error) {e}"
            st.session_state.coach_context_used = False
            st.session_state.coach_recall = []

    # --- Coach box with typing animation ---
    if send_clicked and st.session_state.coach_reply:
        # Animate only on new message
        typewriter_effect(st.session_state.coach_reply)
    else:
        # Keep old message static between reruns
        st.text_area("Coach:", value=st.session_state.coach_reply,
                     height=220, disabled=True)

    # context + recall under the coach box
    st.caption(f"Context used: {st.session_state.coach_context_used}")
    if st.session_state.coach_recall:
        with st.expander("Memory Recall (what the model referenced)"):
            for i, item in enumerate(st.session_state.coach_recall, 1):
                txt = item.get("text", "")
                ts = item.get("ts")
                st.markdown(f"**{i}.** {txt}")
                if ts:
                    st.caption(f"Saved: {ts}")

with c2:
    st.subheader("Add Note")
    note = st.text_area("Write a short note to remember:")
    if st.button("Save Note"):
        try:
            r = requests.post(
                f"{API_BASE}/save_note", json={"user_id": user_id, "text": note}, timeout=180)
            st.success(f"Saved! Note ID: {r.json().get('note_id')}")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.subheader("Daily Check-In")
if st.button("Get Prompts"):
    try:
        r = requests.get(f"{API_BASE}/daily-checkin",
                         params={"user_id": user_id}, timeout=180)
        for i, p in enumerate(r.json().get("prompts", []), 1):
            st.write(f"**{i}.** {p}")
    except Exception as e:
        st.error(f"Error: {e}")
