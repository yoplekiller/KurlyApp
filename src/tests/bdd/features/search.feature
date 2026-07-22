Feature: 검색 기능
  마켓컬리 앱 검색 기능을 검증한다.

  Scenario: 검색 탭 진입 후 검색창 표시
    Given 마켓컬리 앱이 실행되어 있다
    When 검색 탭으로 이동한다
    Then 검색창이 표시된다

  Scenario: 키워드 검색 후 결과 표시
    Given 검색 탭에 진입해 있다
    When 검색창에 "딸기"를 입력한다
    And 검색을 실행한다
    Then "딸기" 검색 결과가 표시된다
