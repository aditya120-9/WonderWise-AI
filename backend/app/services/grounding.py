import re


_CURRENCY_AMOUNT = re.compile(
    r"(?:INR|Rs\.?|₹)\s*[\d,]+(?:\s*(?:-|to)\s*(?:INR|Rs\.?|₹)?\s*[\d,]+)?",
    re.IGNORECASE,
)


def remove_unverified_currency_amounts(answer: str, has_verified_context: bool) -> str:
    if has_verified_context:
        return answer
    return _CURRENCY_AMOUNT.sub("[price not verified]", answer)