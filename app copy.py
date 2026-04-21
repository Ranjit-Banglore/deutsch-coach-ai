import streamlit as st
from llm.openai import openai


st.set_page_config(page_title="AI application", page_icon="🤖")

st.title(" ✨ AI assistant")

st.subheader("Built with ❤️ using OpenAI, Streamlit, Docker and Google Cloud Run.")

#store chat history
if "messages" not in st.session_state:
    st.session_state.messages=[]

# display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# user input 

if prompt := st.chat_input("Ask me anything..."):

    #show user msg
    st.chat_message("user").write(prompt)

    #append prompt to massages history
    st.session_state.messages.append({"role": "user", "content": prompt})

    input= [ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages ]
    
    with st.chat_message("assistant"):
        placeholder=st.empty()
        final_reply=""

        with st.spinner("Thinking..."):
        #reply=openai(input).output[0].content[0].text
            stream=openai(input)

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




