# Test System

import pytest
import pandas as pd
from app import load_data, compute_cosine_similarity, recommend_books, get_filtered_data_and_similarity

@pytest.fixture
def sample_data():
    return load_data()

def test_load_data():
    # Test if data 
    # loads correctly and preprocessing is applied
    data = load_data()
    assert not data.empty, "The DataFrame should not be empty."
    assert 'combined_features' in data.columns, "The 'combined_features' column should exist."

def test_compute_cosine_similarity(sample_data):
    # Test if the cosine similarity matrix is correct
    data = sample_data
    cosine_sim, tfidf_matrix = compute_cosine_similarity(data)
    assert cosine_sim.shape == (tfidf_matrix.shape[0], tfidf_matrix.shape[0]), "Cosine similarity matrix shape should be square based on the number of documents."

def test_recommend_books(sample_data):
    # Test book recommendation function
    
    # Load sample data
    data = sample_data
    
    # Compute cosine similarity
    filtered_data, cosine_sim = get_filtered_data_and_similarity(data, genre='', author='', keyword='')
    recommended_books = recommend_books(cosine_sim, filtered_data)
    
    # Ensure recommendations are not empty
    assert not recommended_books.empty, "Recommendations should not be empty."
    
    # Ensure recommended books have required columns
    assert all(col in recommended_books.columns for col in ['Title', 'Author', 'Image URL']), "Output should include 'Title', 'Author', and 'Image URL'."

# Example of a test that checks for the function handling an empty DataFrame
def test_recommend_books_with_empty_input():
    empty_data = pd.DataFrame()  # Assuming your functions can handle empty DataFrames gracefully
    recommendations = recommend_books(None, empty_data)
    assert recommendations.empty, "Should return an empty DataFrame for empty input."
