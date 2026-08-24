# KulryApp - 마켓컬리 앱 자동화 테스트

Appium 기반 마켓컬리 Android 앱 UI 자동화 테스트 프로젝트입니다.
Jetpack Compose 기반 앱이라 resource-id가 거의 없어, XPath/UiSelector 텍스트 매칭 위주로 로케이터를 구성했습니다.

## 환경

| 항목 | 버전 |
|------|------|
| Device | Samsung Galaxy A32 (SM-A325N) |
| Android | 13 |
| Appium Server | 3.0.1 (UiAutomator2) |
| Appium-Python-Client | 5.3.1 |
| Python | 3.13 |

기기 프로필은 `src/config/device_profiles.json`에 등록하며, `--device-profile` 옵션으로 다른 기기를 지정할 수 있습니다(현재 `galaxy_a32` 1개 등록).

## 설치

```bash
pip install -r requirements.txt
```

## 실행 전 준비

1. 기기 USB 연결 (개발자 모드 + USB 디버깅 활성화)
2. `.env` 파일 생성

```env
# Groq (self-healing 로케이터 제안 + 실패 원인 AI 분석)
GROQ_API_KEY=your_groq_api_key
HEALING_ENABLED=true

# Slack (테스트 실패 알림)
SLACK_WEBHOOK_URL=your_slack_webhook_url
SLACK_NOTIFY_ENABLED=true

# Appium 서버
APPIUM_SERVER_URL=http://127.0.0.1:4723

# 실행할 기기 프로필 (device_profiles.json 키, 기본값 galaxy_a32)
DEVICE_PROFILE=galaxy_a32

# 로그인 실패 테스트용 (정상 로그인 계정은 별도 없음 — 게스트 모드 범위로 제한)
WRONG_TEST_USER_ID=wrong@example.com
WRONG_TEST_USER_PASSWORD=wrong-password
```

3. Appium 서버 실행

```bash
appium
```

## 테스트 실행

```bash
# 전체 실행 (plain + BDD)
pytest

# smoke 테스트만
pytest -m smoke

# 다른 기기 프로필로 실행
pytest --device-profile=galaxy_a32

# BDD 시나리오만
pytest src/tests/bdd/
```

## 프로젝트 구조

```
KulryApp/
├── src/
│   ├── config/
│   │   ├── app_config.py       # capabilities 조립, 타임아웃, 아티팩트 경로
│   │   ├── device_profiles.json # 기기별 capabilities 등록
│   │   └── test_data.py        # 검색 키워드, 오답 계정 등 테스트 데이터
│   ├── pages/                  # Page Object Model
│   │   ├── base_page.py        # 공통 액션 (click/find_element에 self-healing 통합)
│   │   ├── home_page.py
│   │   ├── category_page.py
│   │   ├── search_page.py
│   │   ├── lounge_page.py
│   │   ├── login_page.py
│   │   ├── cart_page.py
│   │   └── product_detail_page.py
│   ├── tests/
│   │   ├── test_home.py           # smoke
│   │   ├── test_category.py       # smoke
│   │   ├── test_search.py
│   │   ├── test_lounge.py         # smoke
│   │   ├── test_login.py          # 로그인 실패 검증 (정상 로그인은 계정 없어 미커버)
│   │   ├── test_cart.py           # smoke
│   │   ├── test_wishlist.py       # smoke, 비로그인(게스트) 범위만
│   │   └── bdd/                   # pytest-bdd 스위트
│   │       ├── features/          # home / category / navigation / search .feature
│   │       ├── test_home_bdd.py
│   │       ├── test_category_bdd.py
│   │       ├── test_navigation_bdd.py
│   │       └── test_search_bdd.py
│   ├── utils/
│   │   ├── popup_handler.py    # 앱 실행 시 팝업 자동 처리
│   │   ├── self_healer.py      # 로케이터 실패 시 Groq LLM이 page_source 기반 대체 로케이터 제안
│   │   ├── failure_analyzer.py # 테스트 실패 원인 Groq 분석
│   │   ├── slack_notifier.py   # 실패 시 Slack Block Kit 알림
│   │   └── logger.py
│   └── conftest.py             # driver fixture(scope=module), --device-profile 옵션
├── .github/workflows/
│   └── appium-selfhosted.yml   # self-hosted 러너 기반 CI (push/workflow_dispatch)
├── reports/                    # pytest-html 리포트
├── screenshots/ / page_sources/ / logs/  # 실패 시 자동 저장
├── pytest.ini
└── requirements.txt
```

## 주요 기능

- **Page Object Model**: 페이지별 로케이터와 액션 분리
- **Self-healing 로케이터**: `click`/`find_element` 실패 시 Groq LLM이 현재 page_source를 보고 대체 로케이터를 제안(`is_visible`/`is_present` 등 상태 확인용 메서드는 대상 아님)
- **AI 실패 분석 + Slack 알림**: 테스트 실패 시 Groq로 원인 2~3문장 분석 후 Slack Block Kit으로 전송
- **BDD 스위트**: pytest-bdd 기반으로 plain pytest와 별도로 핵심 시나리오(home/category/navigation/search) 커버
- **기기 프로필 다중화**: `device_profiles.json` + `--device-profile` CLI 옵션으로 여러 기기 대응 가능한 구조
- **팝업 자동 처리**: 앱 실행 시 뜨는 공지/권한 팝업 자동 닫기
- **CI**: GitHub Actions self-hosted 러너로 push 시 자동 실행 (러너가 오프라인이면 대기 상태로 남음 — 상시 가동 CI는 아님)

## 테스트 시나리오

| 테스트 | 마커 | 설명 |
|--------|------|------|
| `test_home_is_loaded` | - | 홈 화면 정상 로딩 |
| `test_home_has_products` | - | 홈 상품 카드(베스트 탭) 노출 |
| `test_home_scroll_down_and_back` | - | 스크롤 후 하단 탭바 유지 |
| `test_home_has_banner` | - | 홈 배너(ViewPager) 노출 |
| `test_category_tab_opens` | - | 카테고리 탭 진입 |
| `test_category_list_visible` | - | 카테고리 목록(마켓컬리 서브탭 기준) 노출 |
| `test_beauty_kurly_tab_switch` | - | 뷰티컬리 탭 전환 |
| `test_search_tab_opens` | - | 검색 탭 진입 |
| `test_search_has_recommended_keywords` | - | 추천 검색어 노출 |
| `test_lounge_tab_opens` | smoke | 라운지 탭(웹뷰) 진입 |
| `test_lounge_has_content_tabs` | - | 라운지 콘텐츠 탭 노출 |
| `test_login_screen_opens` | - | 로그인 폼 진입 |
| `test_login_with_wrong_credentials` | ⚠️ skip | 오답 계정 로그인 실패 — 운영 서버가 반복 시도 시 에러 알림을 더 이상 노출하지 않아 skip 처리 |
| `test_cart_opens` | smoke | 장바구니 화면 진입 |
| `test_cart_can_close` | - | 장바구니 닫기 |
| `test_wishlist_requires_login` | smoke | 비로그인 상태 찜(픽) 버튼 → 로그인 유도 노출 |
| `test_wishlist_prompt_can_cancel` | - | 로그인 유도 팝업 취소 |

로그인 성공 이후 상태(찜 목록 반영, 주문내역 등)는 테스트 계정이 없어 범위 밖입니다.

## 앱 정보

- Package: `com.dbs.kurly.m2`
- 하단 네비게이션: home / category / search / lounge / mykurly (찜·장바구니 전용 탭 없음)
