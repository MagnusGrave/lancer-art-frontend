import streamlit as st

st.set_page_config(page_title="Unofficial Lancer Assistant", page_icon="🤖", layout="centered")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

import glob
from PIL import Image
from PIL.ExifTags import TAGS
from image_object import ImageObject
from footer import show_footer


##
# Logic
##

# Our method for loading image properties into an array of ImageObject instances.
@st.cache_data()
def instantiate_image_objects():
    image_object_array = []

    for file_path in glob.glob('resources/art/*.jpg'):
        print('file_path: ', file_path)

        im = Image.open(file_path)

        tags = []
        exif_data = im.getexif()
        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            if tag != 'XPKeywords':
                continue

            _data = exif_data.get(tag_id)
            # decode bytes
            if isinstance(_data, bytes):
                data = _data.decode('ascii', 'replace')

                tag_array = ''.join(list(f"{data}")[::2]).rstrip('\x00')
                print()
                print('tag_array: ', tag_array)

                tag_array_split = tag_array.split(';')
                print('tag_array_split: ', tag_array_split)
                print()

                tags = tag_array_split

            if tag == 'XPKeywords':
                break

        print('tags: ', tags)
        print()
        new_image_object = ImageObject(file_path, tags)
        image_object_array.append(new_image_object)

    return image_object_array


# Load all of our art images. This will be called on each state change of the page but
# because it's cached it'll only execute once.
image_objects = instantiate_image_objects()


##
# Setup Sidebar
##

# All possible images tags. Ideally, these would be collected from images upon the first load of the art images.
size_array = [
    'page_full',
    'page_partial',
    'spread_full',
    'spread_partial_mech',
    'spread_partial_scene',
]
composition_array = [
    'full_render',
    'portrait'
]
subjects_array = [
    'pilot',
    'mech',
    'supplies',
    'scenery'
]
theme_array = [
    'life_style',
    'combat'
]


# Sets the state values to include all options
def populate_multi():
    st.session_state.key_size_multiselect = size_array
    st.session_state.key_composition_multiselect = composition_array
    st.session_state.key_subjects_multiselect = subjects_array
    st.session_state.key_theme_multiselect = theme_array
    return


# Sets the state values to empty lists
def clear_multi():
    st.session_state.key_size_multiselect = []
    st.session_state.key_composition_multiselect = []
    st.session_state.key_subjects_multiselect = []
    st.session_state.key_theme_multiselect = []
    return


st.sidebar.header("Filter By Image Tags")
st.sidebar.button('All', on_click=populate_multi)
st.sidebar.button('None', on_click=clear_multi)
size_multiselect = st.sidebar.multiselect('Image Size', size_array, size_array, key='key_size_multiselect')
composition_multiselect = st.sidebar.multiselect('Composition Type', composition_array, composition_array, key='key_composition_multiselect')
subjects_multiselect = st.sidebar.multiselect('Subjects', subjects_array, subjects_array, key='key_subjects_multiselect')
theme_multiselect = st.sidebar.multiselect('Theme', theme_array, theme_array, key='key_theme_multiselect')


##
# Page Content
##

st.title('Art Bible')
st.divider()


def filter_images():
    # Combine the selections of each multiselect into one array
    active_tag_array = [*size_multiselect, *composition_multiselect, *subjects_multiselect, *theme_multiselect]
    print('active_tag_array: ', active_tag_array)

    # Filter the image objects by active tags
    active_tag_set = set(active_tag_array)

    # We don't want a subset, we want to filter if any of the tags are associated with the image
    filtered_image_objects = filter(lambda x: any(tag in active_tag_set for tag in x.tags), image_objects)

    # Show each image via iteration
    for ob in filtered_image_objects:
        st.image(ob.file_path)
        st.caption(str('Tags: ' + ', '.join(ob.tags)))
        st.markdown('#')


# This method will be run anytime there's a change in state on this page.
filter_images()

show_footer()
