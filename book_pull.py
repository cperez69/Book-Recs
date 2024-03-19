import sys
import requests
from bs4 import BeautifulSoup


def get_book_recommendations(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers) # Fetches webpage content

    if response.status_code == 200:
        # Parse HTML    
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        # Find book recommendations based on HTML structure
        recommendations = soup.find_all('div', class_='book')
        for recommendation in recommendations:
            # Extract information requested.
            title_element = recommendation.find('a', class_='bookTitle')
            title = title_element.text.strip()
            book_url = 'https://www.goodreads.com/search?utf8=%E2%9C%93&query=book+recommendations' + title_element['href']
            author = recommendation.find('a', class_='authorName').text.strip()
            description = recommendation.find('span', class_='short').text.strip()

            # Extract cover image URL
            cover_image_element = recommendation.find('img', class_='bookImgSimilar')
            cover_image_url = cover_image_element['src']       
            """" ADD/RMV AFTER I TEST OTHER SECTION
            title = recommendation.find('h2').text.strip()
            author = recommendation.find('p', class_='author').text.strip()
            description = recommendation.find('p', class_='description').text.strip()
            """
            print("Title:", title)
            print("Author:", author)
            print("Description:", description)
            print("Book URL:", book_url)
            print("Cover Image URL:", cover_image_url)
            print("----")
    else:
        print("Failed to retrieve webpage.")

if __name__ == "__main__":
    # Check if URL argument is provided
    if len(sys.argv) != 2:
        print("Usage: python Final_Project.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    get_book_recommendations(url)