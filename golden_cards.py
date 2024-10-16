# golden_cards.py

import random


def assign_golden_cards(board, percentage=0.3):
    """
    전체 타일 중에서 주어진 비율(기본 30%)만큼 랜덤하게 황금카드 타일을 선택하여
    특수 상황을 부여합니다.
    """
    num_golden_cards = int(len(board) * percentage)
    golden_card_positions = random.sample(range(len(board)), num_golden_cards)

    # 황금카드 특수 상황 부여
    golden_cards = {}
    for position in golden_card_positions:
        golden_cards[position] = get_special_effect()

    return golden_cards


def get_special_effect():
    """
    랜덤하게 특수한 상황을 반환합니다.
    """
    random_steps = random.randint(1, 6)
    effects = [
        f"앞으로 {random_steps}칸 이동",
        f"뒤로 {random_steps}칸 이동",
        "다음 턴을 건너뜀",
        "주사위를 다시 굴림",
        "추가 턴 획득",
        "5점 잃음",
        "다음 주사위 결과 두 배",
        "은행에서 10만 원 지급",
        "은행에서 20만 원 지급",
        "은행에서 30만 원 지급",
        "은행에서 40만 원 지급",
        "은행에서 50만 원 지급",
        "은행에 5만 원 지불",
        "은행에 10만 원 지불",
        "은행에 15만 원 지불",
        "은행에 20만 원 지불",
        "은행에 25만 원 지불",
    ]
    return random.choice(effects)


def apply_special_effect(effect, player, board_length):
    """
    주어진 효과를 플레이어에게 적용합니다.
    """
    if "앞으로" in effect:
        steps = int(effect.split(" ")[1].replace("칸", ""))
        player.position = (player.position + steps) % board_length
    elif "뒤로" in effect:
        steps = int(effect.split(" ")[1].replace("칸", ""))
        player.position = (player.position - steps) % board_length
    elif effect == "다음 턴을 건너뜀":
        player.skip_turn = True
    elif effect == "주사위를 다시 굴림":
        return "reroll"
    elif effect == "추가 턴 획득":
        return "extra_turn"
    elif effect == "다음 주사위 결과 두 배":
        player.double_next_roll = True
    elif "은행에서" in effect and "지급" in effect:
        amount = int(effect.split(" ")[1].replace("만", "0000"))
        player.cash += amount
        print(
            f"{player.name}님이 은행에서 {amount}원을 받았습니다! 현재 잔액: {player.cash}원"
        )
    elif "은행에" in effect and "지불" in effect:
        amount = int(effect.split(" ")[1].replace("만", "0000"))
        if player.cash < amount:
            # 현금이 부족하면 부동산을 판매하여 충당
            while player.cash < amount and player.properties:
                # 가장 저렴한 부동산을 판매
                player.properties.sort(key=lambda x: x.calculate_property_value())
                cheapest_property = player.properties.pop(0)
                sale_price = cheapest_property.sell_to_bank()
                player.cash += sale_price
                print(
                    f"{player.name}님이 {cheapest_property.name}을(를) {sale_price}원에 판매했습니다."
                )

            # 현금과 부동산 모두로도 충당되지 않으면 파산 처리
            if player.cash < amount:
                print(f"{player.name}님은 파산하셨습니다.")
                player.is_bankrupt = True
                return None

        # 지불할 수 있는 경우 통상적인 현금 차감
        player.cash -= amount
        print(
            f"{player.name}님이 은행에 {amount}원을 지불했습니다. 현재 잔액: {player.cash}원"
        )
    return None
