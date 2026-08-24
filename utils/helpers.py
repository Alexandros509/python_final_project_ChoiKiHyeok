# utils/helpers.py
# import time이 아닌 datetime
import datetime

class Validation:
    def log_error(error_message):
    #  error_time = datetime.datetime() .now() 추가
       error_time = datetime.datetime.now()
       with open("log.txt", "a", encoding="UTF-8") as fp:
             fp.write(f"[{error_time.strftime('%Y. %m. %d. | %H:%M:%S')}] {error_message}\n")

    def validate_input_text(invalid_text):
       while True:
             text = input(invalid_text).strip()
             if not text:
                print("공백은 입력할 수 없습니다. 다시 입력해주세요.")
                log_error("입력 오류: 공백 입력")
                continue
             # 반환값을 잊어 무한 루프에 빠졌었음
             return text

class Formatting:
    # ISBN 13자리 문자열 포맷팅 (예: 123-45-6789-012-3)
    def format_isbn(isbn_str):
       if len(isbn_str) == 13:
            #return f"{isbn_str[:3]}-{isbn_str[3:5]}-{isbn_str[5:10]}-{isbn_str[10:12]}-{isbn_str[13]}"
            return f"{isbn_str[:3]}-{isbn_str[3:5]}-{isbn_str[5:10]}-{isbn_str[10:12]}-{isbn_str[12]}"
       return isbn_str