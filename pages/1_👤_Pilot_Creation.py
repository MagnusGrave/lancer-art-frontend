import streamlit as st

st.set_page_config(page_title="Unofficial Lancer Assistant", page_icon="👤")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

from footer import show_footer
import requests
import json


##
# Logic
##

# Request raw json files from github repo.
@st.cache_data
def get_data(url_dict):
    json_data_dict = {}
    for url_key in url_dict.keys():
        r = requests.get(url_dict[url_key])
        print(r.text)
        json_data_dict[url_key] = json.loads(r.text)
    return json_data_dict

# Extract a selected properties from an array. top_level_key being the name of the array and second_level_key being the name of a property in those array elements.
@st.cache_data
def get_array_properties(data_dict, top_level_key, second_level_key):
    names = []
    for element in data_dict[top_level_key]:
        names.append(element[second_level_key])
    return names

# Full Dataset
raw_url_dict = {
    'actions': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/actions.json',
    'backgrounds': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/backgrounds.json',
    'pilot_gear': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/pilot_gear.json',
}
lancer_data_dict = get_data(raw_url_dict)

# Granular data
background_choices = get_array_properties(lancer_data_dict, 'backgrounds', 'name')


##
# Setup Sidebar
##


##
# Page Content
##

st.header('Pilot Creation')
st.divider()


st.subheader('Background')

with st.expander("See Background Descriptions"):
    for background in lancer_data_dict['backgrounds']:
        st.text(background['name'])
        st.markdown(background['description'], unsafe_allow_html=True)
        st.markdown('#')

background = st.selectbox("What is your pilot's background?", background_choices)


st.subheader('Skills')
# Choose four skills



show_footer()
