# main.py
from models.base_book import Book
from models.specialized_books import Special_Book 
from utils.helpers import Validation, Formatting
import datetime

# 개별 도서 상세 정보(딕셔너리), 고유 식별 번호 목록(집합)
# 도서가 대여·반납될 때마다 발생하는 데이터(예: ISBN, 처리시간 등)를 변경할 수 없는 튜플(Tuple) 구조로 묶고,
# 이를 리스트(List)에 순차적으로 저장

books = {}
isbn_set = set()
record_history = []

def select_menu():
    # options 일렬로 출력되는 리스트를 `\n`으로 줄바꿈을 시도, 시행착오로 enter로 쉽게 구현할 수 있어 수정.
    options = ["1. 도서 등록",
               "2. 전체 도서 조회",
               "3. 도서 검색",
               "4. 대여/반납 처리",
               "5. 종료"]
    while True:
        print("\n--- 메뉴 ---")
        for opt in options:
            print(opt)
        try:
            choice = input("번호를 입력하세요 (1 ~ 5): ")
            choice_num = int(choice)
            if choice_num < 1 or choice_num > 5:
                raise IndexError
            # choice_num으로 작동하니 인덱스+1로 결과가 나와 수정.
            result = options[choice_num-1]


        except ValueError:
            print("숫자만 입력할 수 있습니다.")  
            Validation.log_error("입력 오류: 숫자 외 입력 ")   
            return         
        except IndexError:
            print("존재하지 않는 인덱스 데이터입니다.")
            Validation.log_error("입력 오류: 인덱스 범위 외 입력 ")
            return   
        else:
            print(f"{result}입니다.")

            if choice =="1":
                register_book()

            elif choice =="2":
                view_all_books()

            elif choice =="3":
                search_books()

            elif choice =="4":
                rental_process()

            else:
                print("종료합니다.")
                break

def register_book():
    print("\n --- 도서등록 ---")
    isbn_raw = input("ISBN을 입력해주세요.\n").strip()
    try:
        int(isbn_raw)

        if len(isbn_raw) != 13:
            raise ValueError("ISBN은 13자리 숫자여야 합니다.")

        if isbn_raw in isbn_set:
            # 타 모듈 함수 호출 시 클래스 이름 포함하여 작성. log_error() X 
            Validation.log_error("입력 오류: ISBN 중복")
            print("존재하는 ISBN입니다.")
            return

        title = Validation.validate_input_text("제목을 입력하세요: ")
        author = Validation.validate_input_text("저자를 입력하세요: ")
        formatted_isbn = Formatting.format_isbn(isbn_raw)

        new_book = Book(title,author,formatted_isbn)
        books[formatted_isbn] = new_book
        isbn_set.add(isbn_raw)
        print(f"[{title}] 도서가 등록되었습니다.")
    except ValueError as e:
        print(f"입력 오류: {e}")
        Validation.log_error(f"ISBN 입력 오류: {e}")
        return

def view_all_books():
    if not books:
        print("등록된 도서가 없습니다.")
        Validation.log_error("입력 오류: 미등록 도서")
        return 
    else:
        print("\n --- 전체 도서 목록 ---")
        for book in books.values():
            print(f"{book.info()}")

def search_books():
    if not books:
        print("등록된 도서가 없습니다.")
        Validation.log_error("검색 오류: 미등록 상태 검색 시도")
        return 

    search_word = Validation.validate_input_text("검색할 제목 혹은 저자를 입력하세요: ")

    for book in books.values():
        # AttributeError: 'Book' object has no attribute '__title'. Did you mean: 'get_title'?
        if search_word in book.get_title() or search_word in book.get_author():
            print(book.info())
        else:
            print("등록되지 않는 도서입니다.")
            Validation.log_error("검색 오류: 미등록 도서 검색")
            return
            
def rental_process():
    if not books:
            print("등록된 도서가 없어 대여/반납 처리를 할 수 없습니다.")
            Validation.log_error("처리 오류: 미등록 도서 대여/반납 시도")
            return
    
    print("\n--- 대여/반납 처리 ---")
    isbn_raw = Validation.validate_input_text("ISBN을 입력해주세요.\n").strip()
    formatted_isbn = Formatting.format_isbn(isbn_raw)

    if formatted_isbn not in books:
        print("등록되지 않은 ISBN입니다.")
        Validation.log_error("처리 오류: 미등록 ISBN 입력")
        return
    rent_target = books[formatted_isbn]

    # 도서: <models.base_book.Book object at 0x0000028C6FE578C0>
    # 제목 호출용 변수 정의해야할듯
    rent_title = books[formatted_isbn].get_title()

    print(f"\n도서: ISBN: {formatted_isbn} 제목: {rent_title}")
    print("1. 대여")
    print("2. 반납")
    rent_choice = Validation.validate_input_text("번호를 선택하세요: ")

    current_time = datetime.datetime.now().strftime('%Y. %m. %d. | %H:%M:%S')

    if rent_choice == "1":
        if rent_target.rent_book():
            rent_history = (formatted_isbn,current_time, "대여")
            record_history.append(rent_history)
            print(f"\n{rent_target.get_title()} 대여를 완료하였습니다.")
        else:
            print("대여 중인 도서입니다.")
            Validation.log_error("대여 실패: 대여 중")
            return

    elif rent_choice == "2":
        if rent_target.return_book():
            return_history = (formatted_isbn,current_time, "반납")
            record_history.append(return_history)
            print(f"\n{rent_target.get_title()} 반납을 완료하였습니다.")
        else:
            print("대여 중인 도서가 아닙니다.")
            Validation.log_error("반납 실패: 미대여 도서")
            return
    else:
        print("잘못된 번호입니다.")
        Validation.log_error("입력 오류: 잘못된 번호")
        return
    
user_choice = select_menu()