import requests

def get_book_genre(isbn):      
    data = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
    if data.status_code == 200:   
        # Get bookname from the response
        book_name = data.json().get('items', [{}])[0].get('volumeInfo', {}).get('title', '')
        return data.json().get('items', [{}])[0].get('volumeInfo', {}).get('categories', [''])[0], book_name
    else:   
        return '', ''
    
        