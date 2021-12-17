"""
This file is the framework for generating multiple Streamlit applications 
through an object oriented framework. 
"""

import logging
from os import listdir
from os.path import isfile, join

# Import necessary libraries
import streamlit as st

st.set_page_config(page_title="Medicinko")

hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}
</style>
"""


# Define the multipage class to manage the multiple apps in our program
class MultiPage:
    """Framework for combining multiple streamlit applications."""

    def __init__(self, directory="./notes") -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
        self.med_dir = directory + "/medical"
        self.tech_dir = directory + "/tech"
        st.markdown(hide_menu, unsafe_allow_html=True)
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

    def _list_all_md_files(self, directory):
        all_files = [f for f in listdir(directory) if isfile(join(directory, f))]
        md_files = [f.split(".md")[0] for f in all_files if f.endswith("md")]
        return md_files

    def initialize_session_vars(self):
        if "med_files" not in st.session_state:
            st.session_state["med_files"] = self._list_all_md_files(self.med_dir)
        if "tech_files" not in st.session_state:
            st.session_state["tech_files"] = self._list_all_md_files(self.tech_dir)
        if "current_choice" not in st.session_state:
            st.session_state["current_choice"] = ""

    def run(self):
        with st.expander("Iskanje", expanded=True):
            domena = st.radio("Domena", options=("Medicina", "Tehnologija"))
            if domena == "Medicina":
                izbrano = st.selectbox(label="", options=st.session_state["med_files"])
                with open(self.med_dir + "/" + izbrano + ".md", "r") as file:
                    tekst = file.read()
            else:
                izbrano = st.selectbox(label="", options=st.session_state["tech_files"])
                with open(self.tech_dir + "/" + izbrano + ".md", "r") as file:
                    tekst = file.read()
            if izbrano != st.session_state["current_choice"] and izbrano != "":
                logging.info(f"User chose [[{izbrano}]]")
                st.session_state["current_choice"] = izbrano

        with st.expander("Zapiski", expanded=True):
            st.markdown(tekst)


# Create an instance of the app
app = MultiPage()

# Title of the main page
st.title("MEDICINKO")

# The main app
app.run()
