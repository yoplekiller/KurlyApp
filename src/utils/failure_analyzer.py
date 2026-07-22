from groq import Groq

_PROMPT_TEMPLATE = """\
당신은 QA 자동화 전문가입니다. Appium 테스트 실패 로그를 분석해주세요.

테스트명: {test_name}
에러 내용:
{error_message}

다음 형식으로 한국어 2~3문장으로 답변하세요:
1. 실패 원인 추정
2. 해결 방법 제안
"""


def analyze_failure(test_name: str, error_message: str, client: Groq) -> str:
    prompt = _PROMPT_TEMPLATE.format(
        test_name=test_name,
        error_message=error_message[:2000],
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()
