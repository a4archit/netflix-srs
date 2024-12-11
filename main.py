import streamlit as st
import pathlib
import pickle
import pandas as pd
import numpy as np
import urllib.parse

# importing datasets
train_data = pickle.load(open('_kaggle_working_train_data.pkl', 'rb'))
data = pd.read_csv('netflix_titles.csv')
churn_1 = pickle.load(open('x_similarity_score_churn_1.pkl','rb'))
churn_2 = pickle.load(open('x_similarity_score_churn_2.pkl','rb'))
similarity_score = np.concatenate([churn_1, churn_2])
# similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

# # ----------- Adding HTML, CSS & JS files to the streamlit ------------- #
# html_file_content = pathlib.Path("index.html").read_text()
# css_file_content = pathlib.Path("style.css").read_text()
# js_file_content = pathlib.Path("script.js").read_text()
# # adding files content to webpage
# st.markdown(html_file_content, unsafe_allow_html=True)
# st.markdown(f"<style>{css_file_content}</style>", unsafe_allow_html=True)
# st.markdown(f"<script>{js_file_content}</script>", unsafe_allow_html=True)

# ------------------------ Python functions ----------------- #
def get_netflix_search_url(movie_title):
    base_url = "https://www.netflix.com/search?q="
    encoded_title = urllib.parse.quote(movie_title)
    return base_url + encoded_title

def clear_input_fields():
    st.session_state.input_label = None

def recommend(show_or_movie_name):
    index = train_data[train_data['title'] == show_or_movie_name].index[0]
    distances = sorted(
        list(enumerate(similarity_score[index])),
        reverse = True, 
        key = lambda x: x[1]
    )[1:6]
    result = []
    for i in distances:
        result.append(train_data.iloc[i[0]].title)
    return result


# ------------------- Streamlit area -------------------- #

st.header("Netflix SRS", divider=True)

st.write("Netflix Shows Recommender System(SRS) will help you to choose Netflix show based on your choices.")

st.subheader("Get your favorite shows instant")
shows_name = st.text_input(
    "",
    key = "input_label",
    placeholder="Enter Netflix TV Show or Movie here"
)
submit_btn = st.button(
    "Recommend", 
    key = "recommendation_btn",
    use_container_width=True, type='primary'
)
submit_btn = st.button(
    ":material/close:", 
    key = "clear_btn",
    use_container_width=True,
    on_click=clear_input_fields
)
# when user click 'Recomend' button
if st.session_state.recommendation_btn == True:
    try:
        results = recommend(shows_name.title())
    except :
        result = None

    if result is None:
        st.write("Invalid TV Show or Movie Name")
        st.write(data.sample(5)['title'])
    else:
        for recommendation in results:
            # extracting information
            xdata = data[data['title'] == recommendation]
            title = xdata['title'].iloc[0]
            type_ = xdata['type'].iloc[0]
            cast = xdata['cast'].iloc[0]
            country = xdata['country'].iloc[0]
            release_year = xdata['release_year'].iloc[0]
            duration = xdata['duration'].iloc[0]
            description = xdata['description'].iloc[0]
            url = get_netflix_search_url(title)

            st.info(f"### :material/arrow_right_alt: **{title}**\
            \n\n[Watch on Netflix]({url}) \
            \n\nType: {type_} \
            \nCountry: {country} \
            \nRelease year: {release_year} \
            \nDuration: {duration} \
            \nCast: {cast} \
            \n\nDescription: {description} \
            ")

