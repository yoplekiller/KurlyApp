Feature: 홈 화면
  마켓컬리 앱 홈 화면의 기본 UI 요소를 검증한다.

  Scenario Outline: 홈 화면 필수 UI 요소 표시
    Given 마켓컬리 앱이 실행되어 있다
    When 홈 화면에 진입한다
    Then 홈 화면에 <element> 노출

    Examples:
      | element     |
      | 하단 탭바   |
      | 상품 섹션 탭 |
      | 상단 배너   |

  Scenario: 홈 화면 스크롤 후 탭바 유지
    Given 마켓컬리 앱이 실행되어 있다
    When 홈 화면에서 아래로 스크롤한다
    And 홈 화면에서 위로 스크롤한다
    Then 하단 탭바가 표시된다
