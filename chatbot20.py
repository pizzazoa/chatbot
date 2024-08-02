import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("스무고개 챗 봇")
st.write(
    "똑똑한(?) 인공지능과 함께 스무고개를 해보세요!"
)

st.write("Please enter your OpenAI API key below.")
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Initiallization
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "ai_question" not in st.session_state:
        st.session_state.ai_question = ""

    # Restart the game
    if st.button("다시 시작", type="primary"):
        st.session_state.clear()
        st.session_state.messages = []
        st.session_state.attempts = 0
    
    # Select Challenger or Tester
    Play = st.radio(
        "문제를 내시겠습니까? 아니면 맞추시겠습니까?",
        ["출제자", "도전자"],
        captions=[
            "GPT가 문제를 맞출겁니다!",
            "GPT의 생각을 맞춰보세요!"
        ],
    )

    st.session_state.attempts = 0
    if Play == "출제자":
        st.write("출제자를 선택하셨습니다!")
        # Display the existing chat messages via `st.chat_message`.
        st.session_state.messages.append({"role": "system", "content": "You are playing 20 Questions. Ask yes or no questions to guess the object the user is thinking of."})
        
        for message in st.session_state.messages:
            if message["role"] != "system":  # Filter out system messages
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

        if prompt := st.chat_input("네 또는 아니오로 답해주세요!"):
            # Store and display the current prompt.
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
        
        st.session_state.attempts += 1

        if st.session_state.attempts >=20:
            st.session_state.messages.append({"role": "system", "content": "You failed. Wait user's behaviour."})
            st.write("You win!")
        
    else:
        st.write("도전자를 선택하셨습니다!")
        st.session_state.messages.append({"role": "system", "content": "You are playing 20 Questions. Think something only one and answer 'yes' or 'no' for questions the user asks."})
        
        # Display the existing chat messages via `st.chat_message`.
        for message in st.session_state.messages:
            if message["role"] != "system":  # Filter out system messages
                with st.chat_message(message["role"]):
                     st.markdown(message["content"])

        
        if prompt := st.chat_input("질문하세요!"):
            # Store and display the current prompt.
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate a response using the OpenAI API.
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            # Stream the response to the chat using `st.write_stream`, then store it in 
            # session state.
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
