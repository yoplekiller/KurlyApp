# KulryApp - 마켓컬리 앱 자동화 테스트

Appium 기반 마켓컬리 Android 앱 UI 자동화 테스트 프로젝트입니다.

## 환경

| 항목 | 버전 |
|------|------|
| Device | Samsung Galaxy S24 Ultra (SM-S928N) |
| Android | 16 |
| Appium | 3.0.1 |
| UiAutomator2 | 5.0.0 |
| Python | 3.13 |

## 설치

```bash
pip install -r requirements.txt
```

## 실행 전 준비

1. 기기 USB 연결 (개발자 모드 + USB 디버깅 활성화)
2. `.env` 파일 생성

```env
KURLY_APP_PACKAGE=com.dbs.kurly.m2
KURLY_APP_ACTIVITY=.a_new_presentation.start.AppStarterActivity
APPIUM_DEVICE_NAME=SM-S928N
ANDROID_PLATFORM_VERSION=16

TEST_USER_ID=your_id
TEST_USER_PASSWORD=your_password
WRONG_TEST_USER_ID=wrong@example.com
WRONG_TEST_USER_PASSWORD=wrongpassword
```

3. Appium 서버 실행

```bash
appium
```

## 테스트 실행

```bash
# 전체 실행
pytest

# smoke 테스트만
pytest -m smoke

# regression 테스트만
pytest -m regression

# 이미지 검증만
pytest -m image_validation
```

## 프로젝트 구조

```
KulryApp/
├── src/
│   ├── config/
│   │   ├── app_config.py       # Appium 설정, 경로, 타임아웃
│   │   └── test_data.py        # 검색 키워드 등 테스트 데이터
│   ├── pages/                  # Page Object Model
│   │   ├── base_page.py        # 공통 액션 (click, input, swipe 등)
│   │   ├── kurly_app_home_page.py
│   │   ├── kurly_app_login_page.py
│   │   ├── kurly_app_search_page.py
│   │   ├── kurly_app_category_page.py
│   │   ├── kurly_app_cart_page.py
│   │   └── kurly_app_my_tab_page.py
│   ├── tests/
│   │   ├── test_home.py           # smoke
│   │   ├── test_search.py         # smoke, regression
│   │   ├── test_login_negative.py # 로그인 실패 검증
│   │   ├── test_category.py       # smoke
│   │   ├── test_my_tab.py         # smoke
│   │   └── test_image_validation.py
│   ├── utils/
│   │   ├── context_manager.py  # WebView/Native 컨텍스트 전환
│   │   ├── popup_handler.py    # 앱 실행 시 팝업 자동 처리
│   │   ├── page_source_helper.py
│   │   └── logger.py
│   ├── conftest.py             # pytest fixtures
│   └── run_smoke.py            # 빠른 수동 확인용 스크립트
├── reports/                    # pytest-html 리포트
├── screenshots/                # 테스트 실패 시 자동 저장
├── page_sources/               # 테스트 실패 시 자동 저장
├── logs/
├── pytest.ini
└── requirements.txt
```

## 주요 기능

- **Page Object Model**: 페이지별 로케이터와 액션 분리
- **WebView/Native 전환**: 컬리 앱 특성에 맞게 컨텍스트 자동 전환
- **팝업 자동 처리**: 앱 실행 시 권한 요청, 공지 팝업 자동 닫기
- **실패 아티팩트 저장**: 테스트 실패 시 스크린샷 + page source 자동 저장
- **HTML 리포트**: `reports/report.html`

## 테스트 시나리오

| 테스트 | 마커 | 설명 |
|--------|------|------|
| test_home_loads | smoke | 홈 화면 정상 로딩 |
| test_home_has_products | smoke | 홈 상품 카드 노출 |
| test_search_returns_results | smoke | 정상 키워드 검색 결과 노출 |
| test_search_with_no_result_keyword | regression | 결과 없는 키워드 검색 시 빈 화면 노출 |
| test_login_with_wrong_credentials | - | 잘못된 계정 로그인 시 로그인 화면 유지 |
| test_category_tab | smoke | 카테고리 탭 진입 및 목록 노출 |
| test_my_tab_opens | smoke | 마이탭 진입 및 콘텐츠 노출 (로그인/비로그인) |
| test_home_has_no_broken_images | image_validation | 홈 화면 깨진 이미지 없음 |

## 앱 정보

- Package: `com.dbs.kurly.m2`
- Main Activity: `.a_new_presentation.start.AppStarterActivity`
