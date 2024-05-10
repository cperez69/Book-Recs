import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://time.com/collection/must-read-books-2023/")

# Wait for the popup to be visible and ensure it is interactable
wait = WebDriverWait(driver, 20)
close_button = wait.until(EC.element_to_be_clickable((By.ID, "close_icon")))

# Click the close button to close the popup
close_button.click()
print("Popup closed.")  # Confirmation message that the popup has been closed

# Wait a moment for the popup to close and page to settle
time.sleep(2)

# Initialize an empty list to store book data
book_data = []

# Find all book entries
books = driver.find_elements(By.CSS_SELECTOR, ".section-list__item > article > a")

# Loop through each book entry and extract the details
for book in books:
    # Open the book link in a new tab
    link_url = book.get_attribute('href')
    driver.execute_script("window.open(arguments[0]);", link_url)

    # Wait and ensure that the new window is opened
    time.sleep(1)  # Giving a moment for the new window to open
    window_handles = driver.window_handles
    if len(window_handles) > 1:
        new_window_handle = window_handles[1]
        driver.switch_to.window(new_window_handle)
    else:
        print("Failed to open new window.")
        continue

    # Check and close any popup that appears
    try:
        close_button = wait.until(EC.element_to_be_clickable((By.ID, "close_icon")))
        close_button.click()
        print("Popup closed on detail page.")
    except:
        print("No popup to close on detail page.")

    # Wait and extract the book details from the detail page
    title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".headline"))).text
    author = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".secondary-title"))).text

    # Find all paragraph elements within the 'padded' class div
    paragraphs = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#article-body .padded p")))

    # Initialize description
    description = ''

    # Handling drop caps and text extraction
    for i, p in enumerate(paragraphs):
        # Check if the paragraph contains a drop cap
        dropcap = p.find_elements(By.CSS_SELECTOR, "span.dropcap")
        if dropcap:
            # If drop cap exists, combine it with the rest of the paragraph text excluding the drop cap span
            dropcap_text = dropcap[0].text
            rest_of_paragraph = p.text[len(dropcap_text):]  # Skip the dropcap length to avoid duplicating the letter
            full_text = dropcap_text + rest_of_paragraph
            description += (full_text if i == 0 else ' ' + full_text)
        else:
            # If no drop cap, append the paragraph normally
            description += (' ' + p.text if i > 0 else p.text)

    # Trim any excess whitespace from the description
    description = description.strip()

    image_url = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "img.fix-layout-shift"))).get_attribute("src")

    words = description.split()
    if words and len(words[0]) == 1:  # Check if the first word is a single letter
        if len(words) > 1:
            description = words[0] + words[1] + ' ' + ' '.join(words[2:])
        else:
            description = words[0]  # Handle unlikely case where description is only one word

    # Print extracted details for checking
    print("Title:", title)
    print("Author:", author)
    print("Description:", description)
    print("Image URL:", image_url)
    # Append to list as a dictionary
    book_data.append({'Title': title, 'Author': author, 'Description': description, 'Image URL': image_url})

    # Close the current tab
    driver.close()

    # Ensure you switch back to the main window correctly
    if len(driver.window_handles) > 0:
        main_window_handle = driver.window_handles[0]
        driver.switch_to.window(main_window_handle)
    else:
        print("Main window is not available.")
        break

# Convert list to DataFrame
df_books = pd.DataFrame(book_data)

# Save the DataFrame to CSV
df_books.to_csv('book_data.csv', index=False)
print("Data saved to CSV.")

# Close the browser
driver.quit()
