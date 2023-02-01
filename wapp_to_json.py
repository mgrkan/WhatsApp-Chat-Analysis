import json
import re
from io import StringIO

def wapp_to_json(chat_location):

    pattern = "([1-9]|1[0-2])/([1-9]|[1-2][0-9]|3[0-1])/([1-9][1-9]), ([0-1][0-9]|2[0-3]):([0-5][0-9]) - "

    chat = StringIO(chat_location)
    chat = chat.readlines()

    chat_json = []
    for i in chat:
        msg_arr = re.split(pattern, i)            
        msg_arr.pop(0)
        
        try:
            msg = msg_arr[5]
        except: continue
        
        b = ""
        for a in msg:
            if(a == ":"):
                break
            a = b + a
            b = a
        msg = msg.replace((b + ": "), "")
        msg_dict = { "Sender": b, "Day": msg_arr[1], "Month": msg_arr[0], 
        "Year": msg_arr[2], "Hour": msg_arr[3], "Message": msg  }

        flag = 1
        for i in ["changed this group", "left", "added",
        "joined using this group's invite link", "removed", "can message this group",
        "ERROR", "changed the subject", "changed the group", "Messages and calls are end-to-end encrypted",
        "created group", "You're now", "started a call", "<Media omitted>"]:
            if i in msg_dict["Sender"]:
                flag = 0
        if flag == 1:
            chat_json.append(msg_dict)
        else:
            continue

    chat_json = json.dumps(chat_json, ensure_ascii=False)
    return chat_json
