from wapp_to_json import wapp_to_json
import json
import streamlit as st
import pandas as pd
from io import StringIO
import plotly.express as px

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

def month_list(messages, members):
    month_list = {}
    for i in members:
        c = 0
        for x in messages:
            if x["Month"] == str(i):
                c += 1
        month_list.update({i : c})
    return month_list


st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="random"
)

st.title("WhatsApp Chat Analyzer")
st.write("""

WhatsApp Chat Analysis\n
Choose a WhatsApp export below 👇

""")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()

    messages = json.loads(wapp_to_json(string_data))
    members = unique(messages)
    amounts = message_amounts(messages, members)
    
    #sorted_dict = sorted(amounts.items(), key=lambda x:x[1])
    #sorted_dict = dict(sorted_dict)
    #print(sorted_dict)

    months = month_list(messages, range(1,13))
    
    df = pd.DataFrame(amounts.values(), index=amounts.keys(),
    columns=["Members"] )
    
    monthsdf = pd.DataFrame(months.values(), index=[
        "0.1 January", "0.2 February", "0.3 March", "0.4 April", "0.5 May", "0.6 June", "0.7 July", "0.8 August", "0.9 September", "1.0 October", "1.1 November", "1.2 December"
    ])
    
    progress = st.progress(0)
    for i in range(100):
        progress.progress(i + 1)

    st.write("""Members""")
    st.bar_chart(df, height=500)
    st.write(px.pie(values=amounts.values(), names=amounts.keys(), title="Pie Chart of messages per members"))

    st.write("""Months""")
    st.bar_chart(monthsdf, height=500)
