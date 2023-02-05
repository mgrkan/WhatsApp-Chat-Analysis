from wapp_to_json import wapp_to_json
import json
import streamlit as st
import pandas as pd
from io import StringIO
import plotly.express as px
from math import floor

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

def wpmemb(messages, members): #words per member
    words_used = {}
    for i in members:
        words = 0
        for x in messages:
            if x["Sender"] == i:
               words += x["Message"].count(" ") + 1
        words_used.update({i : words}) 
    return words_used

def wpm(msg_amounts, words): #words per message
    wpm = {}
    for i in msg_amounts.keys():
        msg = msg_amounts[i]
        word = words[i]
        wpm.update({i : word/msg})
    return wpm

def fwma(wpm, words): #Message amounts recalculation according to average wpm
    fwma_dict = {}
    sum = 0
    for i in wpm.values():
        sum += i
    global average_wpm
    average_wpm = sum / len(wpm)
    for i in words.keys():
        fwma = words[i] / average_wpm
        fwma = floor(fwma)
        fwma_dict.update({i : fwma})
    return fwma_dict
    
def month_list(messages, members):
    month_list = {}
    for i in members:
        c = 0
        for x in messages:
            if x["Month"] == str(i):
                c += 1
        month_list.update({i : c})
    return month_list

def usr_messages(name, messages):
    user_msg = []
    for i in messages:
        if i["Sender"] == name:
            user_msg.append(i)
    return user_msg

def most_used_word(messages):
    word_list = {}
    for i in messages:
        words = i["Message"].split()
        for x in words:
            try:
                q = word_list[x]
                word_list.update({x : q + 1 })
            except:
                word_list.update({x : 1})

    sorted_word_list = sorted(word_list.items(), key=lambda x:x[1])
    muw = sorted_word_list[-1]
    return [sorted_word_list, muw]


st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="random"
)

st.title("WhatsApp Chat Analyzer")
st.write("""

WhatsApp Chat Analysis\n
Choose a WhatsApp export below 👇 App lang must be English

""")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()

    messages = json.loads(wapp_to_json(string_data))
    members = unique(messages)
    amounts = message_amounts(messages, members)
    words = wpmemb(messages, members)
    wpmsg = wpm(amounts, words)
    fwma = fwma(wpmsg, words)
    
    #sorted_dict = sorted(amounts.items(), key=lambda x:x[1])
    #sorted_dict = dict(sorted_dict)
    #print(sorted_dict)

#    months = month_list(messages, range(1,13))
    
    df = pd.DataFrame(amounts.values(), index=amounts.keys(),
    columns=["Members"] )

    wdf = pd.DataFrame(words.values(), index=words.keys(), columns=["Members"] )
    wpmdf = pd.DataFrame(wpmsg.values(), index=wpmsg.keys(), columns=["Members"] )
    fwmadf = pd.DataFrame(fwma.values(), index=fwma.keys(), columns=["Members"] )
    
#    monthsdf = pd.DataFrame(months.values(), index=[
#        "0.1 January", "0.2 February", "0.3 March", "0.4 April", "0.5 May", "0.6 June", "0.7 July", "0.8 August", "0.9 September", "1.0 October", "1.1 November", "1.2 December"
#    ])
    
    progress = st.progress(0)
    for i in range(100):
        progress.progress(i + 1)

    st.write("""Messages per Member""")
    st.bar_chart(df, height=500)
    st.write("""Words per Member""")
    st.bar_chart(wdf, height=500)
    st.write("""Words per Message""")
    st.bar_chart(wpmdf, height=500)
    st.write("""Message amount recalculation with the average wpm ({})""".format(average_wpm))
    st.bar_chart(fwmadf, height=500)
    st.write(px.pie(values=amounts.values(), names=amounts.keys(), title="Pie Chart of messages per members"))
    st.write("""Most used words of the chat""")
    muw = most_used_word(messages)
    top_ten = muw[0]
    last_ten = len(top_ten) - 10
    top_ten = top_ten[last_ten:]
    df = pd.DataFrame([i[1] for i in top_ten], index=[i[0] for i in top_ten], columns=["Words"])
    st.bar_chart(df, height=500)
    muwp = {} #shares of the most used word usage
    for i in members:
        msgs = usr_messages(i, messages)
        for x in most_used_word(msgs)[0]:
            if x[0] == muw[1][0]:
                 muwp.update({i:x[1]})
                 continue
    st.write(px.pie(values=muwp.values(), names=muwp.keys(), title=("""Pie Chart of the word '{}' usage. (Most used word of the group)""".format(muw[1][0]))))
    
    
    for i in members:
        msgs = usr_messages(i, messages)
        top_ten = most_used_word(msgs)[0]
        last_ten = len(top_ten) - 10
        top_ten = top_ten[last_ten:]
        df = pd.DataFrame([i[1] for i in top_ten], index=[i[0] for i in top_ten], columns=["Words"])
        st.write("""{}'s top ten most used words""".format(i))
        st.bar_chart(df, height=500)
    
#    st.write("""Months""")
#    st.bar_chart(monthsdf, height=500)
