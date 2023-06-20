import streamlit as st


# Footer Acknowledgement
def show_footer():
    st.markdown('#')
    st.markdown('#')
    st.divider()
    st.markdown("*Unofficial Lancer Assistant is not an official Lancer product; it is a third party work, and is not affiliated with Massif Press. "
                "Unofficial Lancer Assistant is published via the Lancer Third Party License.*")
    st.image("resources/design/powered_by_Lancer-02.png")
    st.markdown('Words from the author:')
    st.markdown('All featured artworks are owned by Massif Press and must be used in accordance with the license: https://massifpress.com/legal. '
                'This unofficial web app is intended to enhance, and not replace, the experience of Lancer for fans and players. '
                'Please support the official releases of the game and all its official accompaniments, '
                'including the official companion app:')
    st.markdown('https://massifpress.com/   https://massif-press.itch.io/   https://compcon.app/#/')
    st.markdown('Interested in getting involved in official Lancer development, check out their public projects: https://github.com/massif-press')
