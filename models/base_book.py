# models/base_book.py
class Book:
    def __init__(self,title,author,isbn,rented=False):
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__rented = rented

    def info(self):
        return f"책 제목: [{self.__title}], 저자: [{self.__author}], ISBN: [{self.__isbn}], 대여 여부:[{self.__rented}]"

    # Getter
    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_isbn(self):
        return self.__isbn

    def get_rented(self):
        return self.__rented

    
    # Setter
    def rent_book(self):
        if self.__rented == True:
            return False
        else:
            self.__rented = True
            return True

    def return_book(self):
        if self.__rented == True:
            self.__rented = False
            return True
        else:
            return False

