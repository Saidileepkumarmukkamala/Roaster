from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
import random

PAGE_CONFIG = {"page_title":"Roast Lab", 
               "layout":"centered", 
               "initial_sidebar_state":"auto",
                "page_icon":"😈",
               }

st.set_page_config(**PAGE_CONFIG)

taglines = [
    "Your Burn's Cute, But Here Comes the Rebuttal!",
    "You Roast, I Host - A Sizzling Retort!",
    "Fire Up Your Insults, And Get Ready to Be Grilled!",
    "You May Start the Fire, But I Bring the Heat!",
    "Roast Me if You Can - But Brace for the Pan!",
    "Bring the Zing, Expect the Sting!",
    "Roast, Boast, But Expect a Toast!",
    "Your Best Shot vs. My Hot Pot!",
    "You Bring the Sizzle, I Bring the Blaze!",
    "Pitch a Roast, Expect it to Boomerang!",
    "Dish it Out, But Be Ready to Take It!",
    "Roasting Battle - You Start, I Finish!",
    "Throw a Burn, Catch a Blaze!",
    "Light the Fire, Face the Furnace!",
    "Say it Hot, Get it Blazing!",
    "You Spark, I Ignite!",
    "Start a Roast, Expect a Forest Fire!",
    "If You Can't Stand the Heat, Don't Light the Fire!",
    "Serve a Roast, Get Served the Most!",
    "Roast Me? Brace for the Blaze!",
    "Sizzle Me, If You Dare!",
    "You Kindle, I Ignite!",
    "Your Flame, My Inferno!",
    "Try to Burn, Await the Eruption!",
    "Your Spark, My Wildfire!",
    "Light the Match, I'll Be the Blaze!",
    "You Char, I Engulf!",
    "Fire Away, Await the Explosion!",
    "Ignite the Battle, I'll Illuminate the War!",
    "You Flicker, I Flame!",
    "Bring Your Heat, I'm the Furnace!",
    "Your Ember, My Pyroclasm!",
    "Your Scorch, My Conflagration!",
    "Heat Up the Chat, I'll Melt It Down!",
    "Throw a Fireball, Catch a Meteor!",
    "You Simmer, I Boil Over!",
    "You Fire, I Erupt!",
    "Your Smolder, My Flare!",
    "Give Me Coals, I'll Give You Fireworks!"
]


tag = random.choice(taglines)

if 'responses' not in st.session_state:
    st.session_state['responses'] = [tag]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=5,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""You are the RoastMaster. 
                                                                You will respond to every message with the roastning comeback possible and will try to intentionally make sad of the user. 
                                                                Be verbose in your responses so that you get your point across. 
                                                                Do not use any vulgar or obscene language in the response.""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)


st.markdown("<h1 style='text-align: center; font-family: italic;'><span style='color: #6f42c1;'>Roast</span><span style='background: linear-gradient(to right, #007BFF, #28a745); -webkit-background-clip: text; color: transparent;'> Lab</span></h1>", unsafe_allow_html=True)
st.markdown('<br>' * 2, unsafe_allow_html=True)

response_container = st.container()
textcontainer = st.container()



with textcontainer:
    query = st.text_input("Serve Your Best Roast to the Roaster! ",value='', key="input", help="Enter your message here")
    if query:
        with st.spinner("Heating Up the Roast Oven..."):
            response = conversation.predict(input=f"Query:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)

with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')