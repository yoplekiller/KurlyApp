import pytest
from pages.category_page import CategoryPage
from pages.home_page import HomePage
from pages.search_page import SearchPage


@pytest.fixture(scope="module")
def search(driver):
    page = SearchPage(driver)
    page.navigate()
    return page


@pytest.mark.regression
def test_search_tab_opens(search):
    """검색 탭 진입 시 검색어 입력창이 표시되는지 확인"""
    assert search.is_loaded(), "검색 탭에서 검색어 입력창이 표시되지 않음"


@pytest.mark.regression
def test_search_has_recommended_keywords(search):
    """검색 탭에 추천 검색어 섹션이 표시되는지 확인"""
    assert search.has_recommended_keywords(), "검색 탭에 추천 검색어 섹션이 표시되지 않음"


@pytest.mark.regression
@pytest.mark.smoke
def test_search_returns_results(search):
    """검색어 입력 후 제출하면 결과 화면에 해당 키워드가 노출되는지 확인"""
    search.input_text_to_search("샴푸")
    search.submit_search()
    assert search.has_results("샴푸"), "검색 실행 후 결과 화면에 검색어 관련 콘텐츠가 표시되지 않음"


@pytest.mark.regression
def test_search_no_exact_match_shows_related_products(driver):
    """완전히 일치하는 상품이 없는 검색어를 입력해도 "관련 상품" 안내와 함께 대체 상품이 노출되는지 확인.

    이 앱엔 완전한 "검색 결과 없음" 빈 상태가 없고, 대신 관련 상품 추천으로 폴백한다
    (실기기 조사로 확인). module-scope `search` fixture는 앞선 테스트가 이미 검색을 실행해둔
    상태를 물려받아 입력창이 stale해지므로, 홈으로 재진입해 검색 탭을 새로 여는 방식으로 시작한다.

    검색 탭은 마켓컬리/뷰티컬리 선택 상태를 noReset 세션 간에도 기억한다(실기기 조사로 확인) -
    다른 테스트(예: test_beauty_kurly_tab_switch)가 먼저 뷰티컬리로 전환해뒀으면 이 테스트가
    기대하는 마켓컬리 전용 안내 문구가 안 뜬다. CategoryPage.navigate()가 이미 마켓컬리
    서브탭을 명시적으로 클릭해 초기화하는 로직을 갖고 있어 그대로 재사용한다.
    """
    HomePage(driver).navigate()
    CategoryPage(driver).navigate()
    search = SearchPage(driver)
    search.navigate()
    search.input_text_to_search("zzxxqqweuchsjahdsf12345")
    search.submit_search()
    assert search.has_no_exact_match_message(), "일치하는 상품이 없을 때 관련 상품 안내 문구가 표시되지 않음"


@pytest.mark.regression
def test_blank_search_redirects_to_event_page(driver):
    """검색어 없이 검색을 제출하면 이벤트(프로모션) 페이지로 이동하는지 확인.

    웹 버전과 달리 "검색어를 입력해주세요" 안내 팝업이 뜨지 않고, 검색 탭을 벗어나
    이벤트 웹뷰 화면으로 리다이렉트된다(실기기로 2회 재현 확인). 위와 같은 이유로 홈에서
    검색 탭을 새로 열어 시작하고, 위 테스트와 동일하게 마켓컬리 서브탭으로 먼저 초기화한다
    (뷰티컬리 상태로 남아있으면 리다이렉트 대상이 달라질 수 있음).
    """
    HomePage(driver).navigate()
    CategoryPage(driver).navigate()
    search = SearchPage(driver)
    search.navigate()
    search.submit_blank_search()
    assert search.is_on_event_page(), "빈 검색어 제출 후 이벤트 페이지로 이동하지 않음"
