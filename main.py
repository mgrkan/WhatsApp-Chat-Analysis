from wapp_to_json import wapp_to_json
import json
import streamlit as st
import pandas as pd
from io import StringIO

def unique(messages):
    uniques = []
    for i in messages:
        member_name = i["Sender"]
        flag = 0
        for x in uniques:
            if(x == member_name):
                flag = 1
        if flag == 0:
            uniques.append(member_name)
    return uniques

def message_amounts(messages, members):
    msg_amounts = {}
    for i in members:
        c = 0
        for x in messages:
            if x["Sender"] == i:
                c += 1
        msg_amounts.update({i : c})
    return msg_amounts

st.title("WhatsApp Chat Analyzer")
st.write("""

WhatsApp Chat Analysis


""")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()

    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    string_data = stringio.read()

    messages = json.loads(wapp_to_json(string_data))
                    
    members = unique(messages)

    amounts = message_amounts(messages, members)

    df = pd.DataFrame({
        'first column': amounts.keys(),
        'second column': amounts.values()
    })
        
    st.write(df)
