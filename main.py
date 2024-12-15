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
# html_file_content = pathlib.Path("movie_card_ui.html").read_text()
movie_card_ui_css_file_content = pathlib.Path("movie_card_ui_css.css").read_text()
# js_file_content = pathlib.Path("script.js").read_text()
# # adding files content to webpage
# st.markdown(movie_card_ui_css_file_content, unsafe_allow_html=True)
st.markdown(f"<style>{movie_card_ui_css_file_content}</style>", unsafe_allow_html=True)
# st.markdown(f"<script>{js_file_content}</script>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ------------------ Sidebar -------------------------- #

st.sidebar.title("About the developer")
st.sidebar.divider()
st.sidebar.write("I am try to create this web application through the use of \
**Streamlit** with **HTML** and **CSS**. You can check my social media accounts: ")
st.sidebar.write("[Kaggle](https://www.kaggle.com/architty108)")
st.sidebar.write("[Github](https://www.github.com/a4archit)")
st.sidebar.write("[LinkedIn](https://www.linkedin.com/in/archit-tyagi-191323296)")


# ------------------------ Python functions ----------------- #
def get_html_of_cast(cast):
    html_str = ""
    for i, v in enumerate(cast.split(',')):
        if i > 2:
            return html_str
        html_str += f"<li>{v}</li>"
    return html_str

def get_html_content_for_movie_card_ui(title, type_, release_year, duration, director,country, cast, description, url) -> str:
    
    html_movie_card_ui = f"""
    <div class="card">
    <h1>{title}</h1>
        <div class="tags">
            <span class="tag">{type_}</span>
            <span class="tag">{release_year}</span>
            <span class="tag">{duration}</span>
        </div>
        <div class="content">
            <div class="left-section">
                <p><span class="label">Director:</span> {director}</p>
                <p><span class="label">Country:</span> {country}</p>
                <p><span class="label">Casts:</span></p>
                <ul>
                    {get_html_of_cast(cast)}
                </ul>
            </div>
            <div class="right-section">
                <p><span class="label">Description:</span></p>
                <p>{description}</p>
            </div>
        </div>
        <div class="btn-container">
            <a href="{url}" class="btn">Watch now on Netflix</a>
        </div>
    </div>
    """
    return html_movie_card_ui

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


col1, col2 = st.columns(2)
with col1:
    submit_btn = st.button(
        "Recommend", 
        key = "recommendation_btn",
        use_container_width=True, type='primary'
    )

with col2:
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
        results = None

    if results is None:
        st.write("Invalid TV Show or Movie Name")
        random_indian_titles = data[data['country'].apply(lambda x: str(x).lower())=='india'].sample(6)['title'].reset_index(drop=True).iloc[1:].rename('Indian TV Shows/Movies')
        st.write(random_indian_titles)
    else:
        for recommendation in results:
            # extracting information
            xdata = data[data['title'] == recommendation]
            title = xdata['title'].iloc[0]
            type_ = xdata['type'].iloc[0]
            cast = xdata['cast'].iloc[0]
            director = xdata['director'].iloc[0]
            country = xdata['country'].iloc[0]
            release_year = xdata['release_year'].iloc[0]
            duration = xdata['duration'].iloc[0]
            description = xdata['description'].iloc[0]
            url = get_netflix_search_url(title)

            st.markdown(
                get_html_content_for_movie_card_ui(title, type_, release_year, duration, director, country, cast, description, url),
                unsafe_allow_html = True
            )

        st.write("Your feedback: ")
        feedback = st.feedback("stars")
        if feedback is not None:
            feedback_data = pd.read_csv(r"feedback_data.csv")
            new_feedback = {'rating':int(feedback)}
            feedback_data = feedback_data.append(new_feedback, ignore_index=True)
            feedback_data.to_csv('feedback_data.csv')            




