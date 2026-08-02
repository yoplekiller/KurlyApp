# 마켓컬리 Appium 프로젝트 이해하기

> 이 문서는 "어떻게 돌아가는지" 훑어보기 위한 가이드입니다. 코드를 전부 외울 필요는 없고,
> "이 기능이 어디서 시작해서 어디로 흘러가는지" 흐름만 잡으면 충분합니다.

## 1. 전체 구조

```
src/
  config/
    app_config.py       # 환경변수(.env) + device_profiles.json 읽어서 설정값 제공
    device_profiles.json
  pages/                 # Page Object Model
    base_page.py         # 모든 페이지가 상속하는 공통 액션(click, find_element 등)
    home_page.py
    category_page.py
    search_page.py
  utils/
    popup_handler.py     # 앱 실행 직후 팝업(권한요청, 공지 등) 자동 닫기
    self_healer.py       # 로케이터 실패 시 Groq에게 대체 로케이터 물어보기
    failure_analyzer.py  # 테스트 실패 시 Groq에게 실패 원인 물어보기
    slack_notifier.py    # 실패 내용을 Slack Block Kit 메시지로 전송
    logger.py
  tests/
    test_home.py, test_category.py       # 일반 pytest 스타일 테스트
    bdd/                                  # 같은 내용을 BDD(Given-When-Then) 스타일로 재구현
      features/*.feature                  # 시나리오를 자연어로 기술
      test_*_bdd.py                       # feature의 각 문장을 실제 코드에 연결(step definition)
      conftest.py                         # home_page/category_page/search_page fixture 정의
  conftest.py            # driver(Appium 세션) fixture + 실패 시 Slack 알림 훅
```

**핵심 원칙: 테스트 → Page Object → BasePage → Appium/Selenium API** 순으로 위임합니다.
테스트 코드는 "무엇을 확인할지"만 쓰고, "어떻게 클릭/조회하는지"는 Page Object가, "WebDriverWait를
어떻게 거는지" 같은 저수준 동작은 BasePage가 담당합니다. 이게 바로 Page Object Model(POM)의 핵심 —
로케이터가 바뀌어도 Page Object 한 곳만 고치면 되게 만드는 것.

## 2. 테스트 하나가 실행될 때 벌어지는 일 (conftest.py)

```python
@pytest.fixture(scope="module")
def driver(request):
    profile_name = request.config.getoption("--device-profile")
    capabilities = AppConfig.get_capabilities(profile_name)   # ① device_profiles.json에서 기기 설정 읽기
    options = UiAutomator2Options().load_capabilities(capabilities)
    appium_driver = webdriver.Remote(AppConfig.APPIUM_SERVER_URL, options=options)  # ② Appium 서버에 세션 생성 요청
    handle_kurly_popups(appium_driver, wait_time=AppConfig.POPUP_WAIT)              # ③ 초기 팝업 처리
    yield appium_driver                                        # ④ 여기서 실제 테스트들이 실행됨
    appium_driver.quit()                                       # ⑤ 테스트 끝나면 세션 종료
```

- `scope="module"`이라 같은 테스트 파일(module) 안의 테스트들은 driver(앱 세션)를 **공유**합니다.
  즉 매 테스트마다 앱을 새로 켜지 않고, 앱이 켜진 상태에서 여러 테스트를 이어서 돌립니다.
- ①의 `capabilities`는 "어떤 기기에, 어떤 앱을 실행할지"를 Appium 서버에 전달하는 설정 딕셔너리입니다.
  `device_profiles.json`에 기기별로 등록해두고, `--device-profile` 옵션으로 골라 씁니다.

## 3. BasePage — 공통 액션 6종

| 메서드 | 하는 일 | 실패 시 |
|---|---|---|
| `find_element` | 엘리먼트가 DOM에 존재할 때까지 대기 후 반환 | 셀프힐링 시도 |
| `click` | 클릭 가능해질 때까지 대기 후 클릭 | 셀프힐링 시도 |
| `input_text` | `find_element` 호출 후 텍스트 입력 | (find_element 경유라 힐링됨) |
| `is_visible` | 화면에 보이는지 bool로 반환 | 힐링 안 함(아래 참고) |
| `is_present` | DOM에 존재하는지 bool로 반환 | 힐링 안 함 |
| `safe_click` | click 실패해도 예외 안 던지고 bool 반환 | - |

**왜 `is_visible`/`is_present`는 힐링을 안 태울까?**
이 둘은 "없는 게 정상"인 상황(로그인 안 했을 때 버튼이 없어야 함 등)에서도 쓰이는 boolean 체크
메서드입니다. 여기에 힐링을 붙이면 "진짜 없는 것"과 "로케이터가 틀려서 못 찾은 것"을 구분 못 하고
AI가 엉뚱한 걸 찾아 True를 반환할 위험이 있습니다. 그래서 **"반드시 있어야 하는" 액션(click,
find_element, input_text)에만** 힐링을 붙이는 게 원칙입니다. (2026-07-23 리뷰에서 `click`이
이 원칙에서 빠져있던 걸 발견해서 수정 — 아래 4번 참고)

## 4. 셀프힐링 동작 원리 (self_healer.py + base_page.py)

```
click(locator) 호출
  └─ WebDriverWait(...).until(EC.element_to_be_clickable(locator))
       ├─ 성공 → 그대로 클릭
       └─ 실패(TimeoutException) → _try_heal(locator) 호출
              ├─ 현재 화면의 page_source(XML)를 Groq LLM에게 전달
              ├─ "이 로케이터랑 기능적으로 같은 엘리먼트를 XML에서 찾아서 JSON으로 알려줘" 요청
              ├─ 응답을 파싱해서 새 로케이터로 재시도
              └─ 그것도 실패하면 원래 예외를 그대로 raise
```

한 줄 요약: **"이 로케이터로 못 찾으면, 지금 화면 구조를 AI한테 보여주고 비슷한 걸 다시 찾아달라고
한 번 더 물어본다"**가 전부입니다. 새 로케이터를 저장하거나 코드를 자동으로 고치진 않고, 그
테스트 실행 한 번에서만 임시로 사용합니다(런타임 힐링이지, 코드 자동 수정이 아님).

## 5. 실패 시 AI 분석 + Slack 알림 (conftest.py의 pytest 훅)

```
테스트 실패
  └─ pytest_runtest_logreport(report) 훅 실행 (pytest가 자동으로 호출)
       ├─ report.when == "call" 이고 실패했을 때만 동작
       │   (주의: "setup" 단계 실패, 예: 기기 연결 실패는 여기 안 걸림 — 알려진 한계)
       ├─ analyze_failure(): 에러 메시지를 Groq에 보내서 "원인 추정 + 해결 방법" 한국어 2~3문장 받기
       └─ send_failure_alert(): 위 내용을 Slack Block Kit 메시지로 전송
```

`pytest_runtest_logreport`는 일반 함수처럼 누가 호출하는 게 아니라, **pytest가 정해둔 이름의 훅
함수**라서 conftest.py에 이 이름으로 정의만 해두면 pytest가 테스트마다 자동으로 호출해줍니다.

## 6. 팝업 처리 (popup_handler.py)

앱을 처음 켜면 권한 요청, 공지사항 팝업 등이 뜰 수 있습니다. `handle_kurly_popups`는:
1. 이미 홈 화면(`bottom_navigation` 보임)이면 바로 종료
2. 아니면 "권한 팝업 닫기 시도 → 컬리 자체 팝업 닫기 시도"를 최대 5번 반복
3. 그래도 안 되면 뒤로가기 키 1번
4. 그래도 안 되면 앱을 강제로 다시 활성화(`activate_app`)

**주의(코드 주석에 남아있음)**: '닫기' XPath는 예전에 눌렀을 때 앱이 종료돼버려서 제거된 적 있음
— 팝업 버튼을 새로 추가할 땐 실제로 눌러서 앱이 안 꺼지는지 먼저 확인할 것.

## 7. BDD 테스트는 왜 따로 있나 (tests/bdd/)

`test_home.py` 같은 일반 pytest 테스트와 `tests/bdd/test_home_bdd.py`는 **같은 내용을 다른 스타일로
표현한 것**입니다.

- `features/home.feature`: "Given 앱이 실행되어 있다 / When 홈 화면에 진입한다 / Then 하단 탭바가
  표시된다" 처럼 자연어 문장으로 시나리오를 씀 (비개발자도 읽을 수 있게 하는 게 BDD의 목적)
- `test_home_bdd.py`: 각 문장(`@given`, `@when`, `@then`)을 실제 코드와 매칭(= step definition)
- `pages/`, `BasePage`는 그대로 재사용 — BDD는 "테스트를 어떻게 표현하느냐"의 차이일 뿐, 실제
  클릭/검증 로직은 일반 테스트와 동일한 Page Object를 씁니다.

## 8. CI (self-hosted runner)

`.github/workflows/appium-selfhosted.yml`이 push/수동 실행 시 이 PC의 러너에서:
기기 연결 확인 → Appium 서버 기동 → `pytest --device-profile=...` 실행 → 결과물(리포트/스크린샷)
업로드 순으로 돕니다. 클라우드 기기팜 대신 **내 PC를 러너로 등록**해서 이미 로그인된 실기기를
그대로 재사용하는 방식(자세한 이유는 `docs/ci_automation_design.md` 참고).

## 용어 미니 사전 (면접 대비)

| 용어 | 뜻 |
|---|---|
| Page Object Model (POM) | 화면(페이지)마다 클래스를 만들어 로케이터+동작을 캡슐화하는 설계 패턴. UI가 바뀌어도 Page Object만 고치면 되게 하는 게 목적 |
| Locator | 엘리먼트를 찾는 방법. `(By종류, 값)` 튜플. 예: `(AppiumBy.ID, "com.dbs.kurly.m2:id/category")` |
| Capabilities | Appium 세션을 만들 때 "어떤 기기/앱을 어떻게 실행할지" 서버에 전달하는 설정 딕셔너리 |
| Self-healing | 로케이터 실패 시 대체 로케이터를 자동으로 찾아 재시도하는 기법(여기선 LLM 기반) |
| Fixture (pytest) | 테스트에 필요한 준비물(예: driver)을 만들어주는 함수. `yield` 앞은 준비, 뒤는 정리(teardown) |
| Hook (pytest) | `pytest_runtest_logreport`처럼 pytest가 정해진 시점에 자동으로 호출해주는 특수 함수 |
