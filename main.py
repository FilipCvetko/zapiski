"""
This file is the framework for generating multiple Streamlit applications 
through an object oriented framework. 
"""
import re
import requests
import logging
from os import listdir
from os.path import isfile, join
from style import hide_menu, margins, bullets
import json
import time

# Import necessary libraries
import streamlit as st

st.set_page_config(page_title="Medicinko")


DOBOVA_IP = "193.95.248.125:33444"
#DOBOVA_IP = "192.168.1.2:33444"

# Define the multipage class to manage the multiple apps in our program
class MultiPage:
    """Framework for combining multiple streamlit applications."""

    def __init__(self, directory="./notes") -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
        self.med_dir = directory + "/medical"
        self.tech_dir = directory + "/tech"
        st.markdown(hide_menu, unsafe_allow_html=True)
        st.markdown(bullets, unsafe_allow_html=True)
        st.markdown(margins, unsafe_allow_html=True)
        # Initialize a unique session ID
        self.session_id = self._get_session()
        self.initialize_session_vars()
        logging.basicConfig(
            format="[%(asctime)s]::[{}]::[%(levelname)s]::%(message)s".format(
                self.session_id
            ),
            level=logging.INFO,
            force=True,
            filename="./tmp/log.txt",
            filemode="a",
        )
        logging.debug("Successfully initialized MultiPage class")

    def _get_session(self):
        from streamlit.report_thread import get_report_ctx
        from streamlit.server.server import Server

        session_id = get_report_ctx().session_id
        session_info = Server.get_current()._get_session_info(session_id)
        if session_info is None:
            raise RuntimeError("Couldn't get your Streamlit Session object.")
        return str(hash(session_info.session))[6:18]

    def _list_all_md_files(self, domain):
        r = requests.post("http://" + DOBOVA_IP + "/get_fnames", json={"query": domain})
        return json.loads(r.content.decode("utf-8"))["filenames"]

    def initialize_session_vars(self):
        if "med_files" not in st.session_state:
            st.session_state["med_files"] = self._list_all_md_files("medical")
        if "tech_files" not in st.session_state:
            st.session_state["tech_files"] = self._list_all_md_files("tech")
        if "current_choice" not in st.session_state:
            st.session_state["current_choice"] = ""

    def load_current_page(self, response):
        # View text with response.text
        readme_buffer = []
        pattern = r"(w?.png)|(w?.jpg)|(w?.jpeg)"
        for line in response.text.splitlines():

            readme_buffer.append(line)

            if re.search(pattern, line):
                fname = line.strip().rstrip()
                some_str = "\n".join(readme_buffer[:-1])

                st.markdown("".join((some_str)), unsafe_allow_html=True)

                # Perform image logic
                img_request = requests.post(
                    "http://" + DOBOVA_IP + "/get_img_file", json={"fname": fname}
                )

                if img_request.status_code == 200:
                    st.image(img_request.content)
                readme_buffer.clear()

        some_str = "\n".join(readme_buffer)
        st.markdown("".join((some_str)), unsafe_allow_html=True)
        st.write("")

    def run(self):
        with st.expander("Iskanje", expanded=True):
            col1, col2 = st.columns(2)
            domena = col1.radio("Domena", options=("Medicina", "Tehnologija"))
            st.session_state["password"] = col2.text_input("Geslo", type="password")
            if domena == "Medicina":
                izbrano = st.selectbox(label="", options=st.session_state["med_files"])
            else:
                izbrano = st.selectbox(label="", options=st.session_state["tech_files"])

            if domena == "Medicina":
                _domain = "medical"
            if domena == "Tehnologija":
                _domain = "tech"

            if izbrano != st.session_state["current_choice"] and izbrano != "":

                logging.info(f"User chose [[{izbrano}]]")
                st.session_state["current_choice"] = izbrano

        with st.expander("Zapiski", expanded=True):
            if st.session_state["password"] == "gggg":
                r = requests.post(
                    "http://" + DOBOVA_IP + "/get_md_file",
                    json={"fname": izbrano, "domain": _domain},
                )
                if r.status_code == 200:
                    self.load_current_page(r)
            else:
                st.write("Vpiši geslo.")


# Create an instance of the app
app = MultiPage()

# Title of the main page
st.title("MEDICINKO")

# The main app
app.run()
