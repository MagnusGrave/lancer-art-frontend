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


# Extract a selected properties from an array. top_level_key being the name of the array and
# second_level_key being the name of a property in those array elements.
@st.cache_data
def get_array_properties(data_dict, top_level_key, second_level_key):
    names = []
    for element in data_dict[top_level_key]:
        if element[second_level_key] != 'ERR: DATA NOT FOUND':
            names.append(element[second_level_key])
    return names


@st.cache_data
def get_array_properties_filtered(data_dict, top_level_key, second_level_key, second_level_filter_key, filter_value):
    names = []
    for element in data_dict[top_level_key]:
        if element[second_level_filter_key] == filter_value and element[second_level_key] != 'ERR: DATA NOT FOUND':
            names.append(element[second_level_key])
    return names


# Full Dataset
raw_url_dict = {
    'actions': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/actions.json',
    'backgrounds': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/backgrounds.json',
    'core_bonuses': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/core_bonuses.json',
    'environments': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/environments.json',
    'factions': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/factions.json',
    'frames': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/frames.json',
    'glossary': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/glossary.json',
    'info': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/info.json',
    'manufacturers': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/manufacturers.json',
    'mods': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/mods.json',
    'pilot_gear': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/pilot_gear.json',
    'reserves': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/reserves.json',
    'rules': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/rules.json',
    'sitreps': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/sitreps.json',
    'skills': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/skills.json',
    'statuses': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/statuses.json',
    'systems': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/systems.json',
    'tables': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/tables.json',
    'tags': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/tags.json',
    'talents': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/talents.json',
    'weapons': 'https://raw.githubusercontent.com/massif-press/lancer-data/master/lib/weapons.json'
}
lancer_data_dict = get_data(raw_url_dict)

# Granular data
background_choices = get_array_properties(lancer_data_dict, 'backgrounds', 'name')
skill_choices = get_array_properties(lancer_data_dict, 'skills', 'name')
gear_armor_choices = get_array_properties_filtered(lancer_data_dict, 'pilot_gear', 'name', 'type', 'Armor')
gear_weapon_choices = get_array_properties_filtered(lancer_data_dict, 'pilot_gear', 'name', 'type', 'Weapon')
gear_gear_choices = get_array_properties_filtered(lancer_data_dict, 'pilot_gear', 'name', 'type', 'Gear')

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
chosen_background = st.selectbox("What is your pilot's background?", background_choices)
st.markdown('#')


st.subheader('Skills')
with st.expander("See Skill Descriptions"):
    for background in lancer_data_dict['skills']:
        st.subheader(background['name'])
        st.markdown(background['description'], unsafe_allow_html=True)
        st.markdown('*Usage:*<br />' + background['detail'], unsafe_allow_html=True)
        st.markdown('*Governing Stat:*<br />' + background['family'], unsafe_allow_html=True)
        st.markdown('#')
chosen_skills = st.multiselect("Pick 4 skills.", skill_choices, max_selections=4)
st.markdown('#')

st.subheader('Gear')
#st.write(lancer_data_dict['pilot_gear'])
chosen_armor = st.multiselect("Pick your armor.", gear_armor_choices, max_selections=1)
chosen_weapons = st.multiselect("Pick 2 weapons.", gear_weapon_choices, max_selections=2)
chosen_gear = st.multiselect("Pick 3 pieces of gear.", gear_gear_choices, max_selections=3)
st.markdown('#')

show_footer()
