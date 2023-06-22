import streamlit as st

st.set_page_config(page_title="Unofficial Lancer Assistant", page_icon="🔧")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

import common
from footer import show_footer
import plotly.graph_objects as go


##
# Logic
##

(weapons_sheet_df,) = common.load_tables(['weapons_table', ])


def figure_1(dataframe):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dataframe['type'],
        y=dataframe['range_val']
    ))
    fig.update_layout(title='Type vs. Range', xaxis_title='Type', yaxis_title='Range', legend_title_text='Types')

    return fig


##
# Setup Sidebar
##


##
# Page Content
##

st.header('Build your Frame')
st.divider()

st.subheader('Custom Weapons Table')
st.write(weapons_sheet_df)
st.markdown('#')

st.subheader('Example Plot')
st.write(figure_1(weapons_sheet_df))

show_footer()
