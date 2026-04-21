import streamlit as st
from llm.openai import openai
from llm.system_prompt import get_system_prompt

# -----------------------
# CONFIG
# -----------------------

st.set_page_config(
    page_title="DeutschCoach AI 🇩🇪",
    page_icon="🇩🇪",
    layout="wide"
)

# -----------------------
# CUSTOM CSS (Premium Look)
# -----------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}
.user-msg {
    background-color: #1f6feb;
    padding: 10px;
    border-radius: 12px;
}
.assistant-msg {
    background-color: #30363d;
    padding: 10px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# SESSION STATE
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# SIDEBAR (Premium Controls)
# -----------------------
with st.sidebar:
    st.title("⚙️ Settings")

    scenario = st.selectbox(
        "🎭 Scenario",
        ["casual", "interview", "dating", "landlord", "doctor"]
    )

    mode = st.radio(
        "🌐 Mode",
        ["German Only 🇩🇪", "German + English 🇬🇧"]
    )

    correction = st.toggle("✏️ Smart Correction", value=True)

    st.markdown("---")
    st.caption("🇩🇪 Practice real German conversations")

# -----------------------
# HEADER
# -----------------------
st.title("🇩🇪 DeutschCoach AI")
st.caption("Practice real-life German conversations")

# -----------------------
# DISPLAY CHAT HISTORY
# -----------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------
# USER INPUT
# -----------------------
# user input 

if prompt := st.chat_input("Ask me anything..."):

    #show user msg
    st.chat_message("user").write(prompt)

    #append prompt to massages history
    st.session_state.messages.append({"role": "user", "content": prompt})

    input= [ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages ]
    
    #system message

    with st.chat_message("assistant"):
        placeholder=st.empty()
        final_reply=""

        with st.spinner("Thinking..."):
        #reply=openai(input).output[0].content[0].text
            #st.write(f"scenario={scenario}, mode={mode}, correction: {correction}")
            system_prompt=get_system_prompt(scenario,mode,correction)
            #st.write(system_prompt)
            input.append(system_prompt)
            stream=openai(input)
            #st.write(f"scenario={scenario}")
            for chunk in stream:
                delta=chunk.choices[0].delta
                if delta.content:
                    final_reply+=delta.content
                    placeholder.markdown(final_reply+ "▌")

            placeholder.markdown(final_reply)

    #show assistent msg:
    #st.chat_message("assistant").write(final_reply)
    
    #append assistant msg
    st.session_state.messages.append({"role":"assistant", "content":final_reply})
