#Book Recommendation Scrapper
#Sales Pitch
Welcome to GoodReads Book Recommendation scrapper! This script is designed to give you recommendations on book based on your parameters. It will include details such as the title, author, description of the book, book URL for purchase, and cover image URL.

## Functions
The main function of the script is as follows:

get_book_recommendations(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

This should fetch the webpage with certain content pertaining to your book recommendations and return some book info.

## Usage
Here's an example of how you might use this script:

-initialize 'pip list' for requests
- initialize 'pip install beautifulsoup4' - this is for web scrapping

python Final_Project.py <URL>
