import json
import re

from appium.webdriver.common.appiumby import AppiumBy
from groq import Groq

_BY_MAP = {
    "xpath": AppiumBy.XPATH,
    "id": AppiumBy.ID,
    "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR,
    "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
}

_PROMPT_TEMPLATE = """\
You are an Appium Android automation expert.

The following locator failed to find an element:
  type : {by}
  value: {value}

Current UI page source (truncated):
{page_source}

Find the same (or functionally equivalent) element in the XML above and respond \
with ONE JSON object only — no explanation, no markdown:
{{"by": "<xpath|id|android_uiautomator|accessibility_id>", "value": "<locator_value>"}}
"""


def suggest_locator(
    original_locator: tuple[str, str],
    page_source: str,
    client: Groq,
) -> tuple[str, str] | None:
    prompt = _PROMPT_TEMPLATE.format(
        by=original_locator[0],
        value=original_locator[1],
        page_source=page_source[:4000],
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=200,
    )

    raw = response.choices[0].message.content.strip()

    # 마크다운 코드블록 제거 후 JSON 추출
    json_match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not json_match:
        return None

    data = json.loads(json_match.group())
    by = _BY_MAP.get(data.get("by", ""))
    value = data.get("value", "")

    if by and value:
        return (by, value)
    return None
