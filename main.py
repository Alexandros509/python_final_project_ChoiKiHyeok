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
               "5. 종료",
               "6. 통계 조회"]
    while True:
        print("\n--- 메뉴 ---")
        for opt in options:
            print(opt)
        try:
            choice = input("번호를 입력하세요 (1 ~ 6): ")
            choice_num = int(choice)
            if choice_num < 1 or choice_num > 6:
                raise IndexError
            # choice_num으로 작동하니 인덱스+1로 결과가 나와 수정.
            result = options[choice_num-1]


        except ValueError:
            print("숫자만 입력할 수 있습니다.")  
            Validation.log_error("입력 오류: 숫자 외 입력 ")   
            return         
        except IndexError:
            print("범위 내 숫자를 입력해주세요.")
            Validation.log_error("입력 오류: 인덱스 범위 외 입력 ")
            return   
        else:
            print(f"\n{result}입니다.")

            if choice =="1":
                register_book()

            elif choice =="2":
                view_all_books()

            elif choice =="3":
                search_books()

            elif choice =="4":
                rental_process()

            elif choice =="5":
                print("종료합니다.")
                break
            else:
                view_statistic()

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
        # 책 유형 추가
        book_type = Validation.validate_input_text("책 유형을 입력하세요: \n일반 단행본 / 전자 도서\n").strip()
        
        try:
            if book_type not in ("일반 단행본", "전자 도서", "일반단행본", "전자도서"):
                    raise ValueError("올바른 도서 유형을 입력하세요.")
                
        except ValueError as e:
            print(f"입력 오류: {e}")
            Validation.log_error(f"도서 유형 입력 오류: {e}")
            return
        else:
            new_book = Special_Book(title,author,formatted_isbn,book_type,False)
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
            # book_type 추가하며  new_book = Book > Special_Book으로 바뀌며 발생
            # 책 제목: [<bound method Book.get_title of <models.specialized_books.Special_Book object at 0x000001CAE71A78C0>>], 저자: [<bound method Book.get_author of <models.specialized_books.Special_Book object at 0x000001CAE71A78C0>>], ISBN: [<bound method Book.get_isbn of <models.specialized_books.Special_Book object at 0x000001CAE71A78C0>>], 대여 여부:[<bound method Book.get_rented of <models.specialized_books.Special_Book object at 0x000001CAE71A78C0>>], 책 종류: [일반 단행본]
            # print(f"{book.info()}")
            print(f"책 제목: [{book.get_title()}], 저자: [{book.get_author()}], ISBN: [{book.get_isbn()}], 책 유형: [{book.get_book_type()}] , 대여 여부:[{book.get_rented()}]")

def search_books():
    if not books:
        print("등록된 도서가 없습니다.")
        Validation.log_error("검색 오류: 미등록 상태 검색 시도")
        return 

    search_word = Validation.validate_input_text("검색할 제목 혹은 저자를 입력하세요: ")

    for book in books.values():
        # AttributeError: 'Book' object has no attribute '__title'. Did you mean: 'get_title'?
        if search_word in book.get_title() or search_word in book.get_author():
            print(f"책 제목: [{book.get_title()}], 저자: [{book.get_author()}], ISBN: [{book.get_isbn()}], 책 유형: [{book.get_book_type()}], 대여 여부:[{book.get_rented()}]")
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
    
def view_statistic():
    print("\n--- 통계 조회 ---")
    print("1. 월간 대여 통계")
    print("2. Most Popular Book")

    view_stats_choice = Validation.validate_input_text("번호를 선택하세요: ").strip()

    if view_stats_choice == "1":
        # rent_history = (formatted_isbn,current_time, "대여")  튜플
        # record_history.append(rent_history)  리스트
        # current_time의 %m을 어떻게 추출하지?
        # count?
        # (ct.year, ct.month)
        # ct = record_history[]
        # for i in range(1,13):
        #     if ct.month() >=i and ct.month() < i+1:
        #         print(f"{record_history}")
        # 리스트된 튜플들 언패킹
        monthly_stat = {}
        for isbn, time_str, rent_stat in record_history:
            if rent_stat == "대여":
                month_k = time_str[:9]
                stat_k = (month_k,isbn)
                if stat_k in monthly_stat:
                    monthly_stat[stat_k] += 1
                else:
                    monthly_stat[stat_k] = 1
        print("\n--- 월간 도서별 대여 통계 ---")
        for (month, isbn), count in monthly_stat.items():
            print(f"[{month}] ISBN: {isbn} | 제목: {books[isbn].get_title()} | 대여 횟수: {count}건")

    if view_stats_choice == "2":
        pass
        # record_history의 list된 튜플 속의 formatted_isbn을 어떻게든?
        # exs = list.count / tuple.count | exs.format exs.name? 
        rent_count = {}
        for isbn, time_str, rent_stat in record_history:
            if rent_stat == "대여":
                if isbn in rent_count:
                    rent_count[isbn] += 1
                else:
                    rent_count[isbn] = 1
        if not rent_count:
            print("대여 이력이 없습니다.")
            return

        most_popular_isbn = max(rent_count,key=rent_count.get)
        max_rent_count = rent_count[most_popular_isbn]
        print("\n--- Most Popular Book ---")
        print(f"ISBN: {most_popular_isbn} | 제목: [{books[isbn].get_title()}] | 총 대여 횟수: {max_rent_count}회")

user_choice = select_menu()