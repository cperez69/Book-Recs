#Chrome Opener/Web Builder

import streamlit as st  # Importing Streamlit for building web applications
import pandas as pd  # Importing pandas for data manipulation
from sklearn.feature_extraction.text import TfidfVectorizer  # Importing TF-IDF Vectorizer for text processing
from sklearn.metrics.pairwise import cosine_similarity  # Importing cosine similarity for similarity calculation

# Load data and cache it for efficiency
def load_data():
    data = pd.read_csv('updated_book_data.csv')  # Reading the CSV file containing book data
    data['Author'] = data['Author'].str.replace('by ', '', case=False).str.strip()  # Cleaning author names
    data['combined_features'] = data['Title'] + ' ' + data['Author'] + ' ' + data['Description'] + ' ' + data['Genre']  # Combining features for TF-IDF
    return data

# Compute cosine similarity
def compute_cosine_similarity(data):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')  # Creating TF-IDF Vectorizer
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined_features'])  # Fitting and transforming data
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)  # Calculating cosine similarity
    return cosine_sim, tfidf_matrix

# Filter books based on genre, author, and optional keyword
def get_filtered_data_and_similarity(data, genre, author, keyword):
    filtered_data = data
    if genre:
        filtered_data = filtered_data[filtered_data['Genre'].str.contains(genre, case=False, na=False, regex=True)]  # Filtering by genre
    if author:
        filtered_data = filtered_data[filtered_data['Author'].str.contains(author, case=False, na=False)]  # Filtering by author
    if keyword:
        filtered_data = filtered_data[filtered_data['Description'].str.contains(keyword, case=False, na=False)]  # Filtering by keyword
    if filtered_data.empty:
        return None, None
    cosine_sim, _ = compute_cosine_similarity(filtered_data)
    return filtered_data, cosine_sim

def recommend_books(cosine_sim, data):
    if cosine_sim is not None:
        idx = 0
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Sorting similarity scores
        sim_scores = sim_scores[1:4]
        book_indices = [i[0] for i in sim_scores]
        if not book_indices:
            return pd.DataFrame()  # Return empty DataFrame if no book indices found
        return data.iloc[book_indices][['Title', 'Author', 'Image URL']]
    return pd.DataFrame()

def main():
    st.title("📚 Book Recommender System 🌟")
    data = load_data()

    genre = st.selectbox("Choose your preferred genre 📖", ['', 'Fiction', 'History', 'Biography', 'Science', 'Fantasy'])  # Dropdown for selecting genre
    author = st.text_input("Enter preferred author (leave blank if no preference) 🖋️")  # Text input for author name
    keyword = st.text_input("Enter a keyword from the book description (optional) 🔍")  # Text input for keyword

    if st.button("Recommend Books 🚀"):
        filtered_data, cosine_sim = get_filtered_data_and_similarity(data, genre, author, keyword)  # Getting filtered data and similarity
        if filtered_data is not None and not filtered_data.empty:
            recommended_books = recommend_books(cosine_sim, filtered_data)
            if not recommended_books.empty:
                st.write("Based on your preferences, we recommend these books:")
                for index, row in recommended_books.iterrows():
                    st.text(f"Title: {row['Title']} 📘")  # Displaying book title
                    st.text(f"Author: {row['Author']} ✍️")  # Displaying author
                    st.image(row['Image URL'], caption=row['Title'])  # Displaying book image
            else:
                st.write("😢 No recommendations available. Please adjust your filters.")  # No recommendations message
        else:
            st.write("🚫 No books found matching your criteria. Please adjust your filters.")  # No matching books message

if __name__ == "__main__":
    main()
