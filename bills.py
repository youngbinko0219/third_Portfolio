# bills.py

# 지폐 단위 정의 (단위: 만원)
bills = {
    "1만원권": 10000,
    "5만원권": 50000,
    "10만원권": 100000,
    "50만원권": 500000,
    "100만원권": 1000000,
    "200만원권": 2000000,
    "500만원권": 5000000,
}


def get_bill_amount(bill_name):
    """
    지폐 이름으로 해당 금액을 반환합니다.
    bill_name: str - 지폐 이름 (예: "5만원권")
    """
    return bills.get(bill_name, 0)


def calculate_total_amount(bill_counts):
    """
    각 지폐 단위와 개수를 받아 총 금액을 계산합니다.
    bill_counts: dict - {"1만원권": 개수, "5만원권": 개수, ...}
    """
    total = 0
    for bill_name, count in bill_counts.items():
        total += get_bill_amount(bill_name) * count
    return total
