import os

class TestData:
    SEARCH_KEYWORD = os.getenv("SEARCH_KEYWORD", "우유")
    NO_RESULT_KEYWORD = os.getenv("NO_RESULT_KEYWORD", "xyzxyzxyz검색결과없음123")
