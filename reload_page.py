import streamlit as st
import streamlit.ReportThread as ReportThread
from streamlit.server.Server import Server
import pandas as pd
import json
import time

def trigger_rerun():

    ctx = ReportThread.get_report_ctx()

    this_session = None
    
    current_server = Server.get_current()
    if hasattr(current_server, '_session_infos'):
        # Streamlit < 0.56        
        session_infos = Server.get_current()._session_infos.values()
    else:
        session_infos = Server.get_current()._session_info_by_id.values()

    for session_info in session_infos:
        s = session_info.session
        if (
            # Streamlit < 0.54.0
            (hasattr(s, '_main_dg') and s._main_dg == ctx.main_dg)
            or
            # Streamlit >= 0.54.0
            (not hasattr(s, '_main_dg') and s.enqueue == ctx.enqueue)
        ):
            this_session = s

    if this_session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')
    this_session.request_rerun()


def get_latest_data():
    return {
        "features": {
            "feature1": True,
            "feature2": True,
            "threasholdA": time.time()
        },
        "actions": [
            "actOnWarning1",
            "getEvenmoreData"
        ]
    }

latest_data = get_latest_data()

delay_time = st.number_input("Delay", value=5)
other_data = st.text_input("some other thing")



st.write(latest_data)
st.write(other_data)


time.sleep(delay_time)
new_data = get_latest_data()
# Work out your own comparitor
while new_data == latest_data:
    new_data = get_latest_data()
    print(new_data)
    time.sleep(delay_time)

print("No longer equal, rerunning")
trigger_rerun()
