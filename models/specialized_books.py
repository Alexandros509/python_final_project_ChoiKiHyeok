# models/specialized_books.py
# from 모듈 호출 에러. from base_book
from models.base_book import Book

class Special_Book(Book):
    # kwargs는 맨 뒤로
    def __init__(self,title,author,isbn,book_type, rented=False):
        super().__init__(title,author,isbn,rented)
        self.__book_type = book_type

    def info(self):
        return f"책 제목: [{self.get_title}], 저자: [{self.get_author}], ISBN: [{self.get_isbn}], 대여 여부:[{self.get_rented}], 책 종류: [{self.__book_type}]"

    # Getter
    def get_book_type(self):
        return self.__book_type