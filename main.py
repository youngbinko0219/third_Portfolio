# main.py

from tiles import create_tiles
from dice import roll_dice
from player import Player
from bank import Bank
from game_utils import display_welcome_message, check_for_quit, check_end_game
from golden_cards import assign_golden_cards, apply_special_effect


def main():
    # 환영 메시지 호출
    display_welcome_message()

    # 은행, 타일, 플레이어 설정
    bank = Bank()  # 은행 인스턴스 생성
    board = create_tiles()  # 도시 타일 생성
    board_length = len(board)
    players = [Player(f"플레이어 {i+1}") for i in range(4)]

    # 황금카드 설정
    golden_cards = assign_golden_cards(board)
    print("황금카드가 무작위로 지정되었습니다!")

    while True:
        for player in players:
            # 턴 시작 시 파산한 플레이어 제거
            players = [
                player
                for player in players
                if not getattr(player, "is_bankrupt", False)
            ]

            # 게임 종료 여부 확인
            if check_end_game(players):
                return  # 게임 종료

            # 턴 건너뛰기 확인
            if hasattr(player, "skip_turn") and player.skip_turn:
                print(f"{player.name}님은 이번 턴을 건너뜁니다!")
                player.skip_turn = False
                continue

            # 게임 종료 여부 확인
            if check_for_quit(player.name):
                return

            # 주사위 굴리기
            steps = roll_dice()
            print(f"{player.name}님이 {steps}을(를) 굴렸습니다.")

            # 플레이어 이동
            previous_position = player.position
            player.move(steps, board_length)

            # 첫 번째 칸 도착 시 20만 원 지급
            if player.position == 0 and previous_position != 0:
                print(f"{player.name}님이 첫 번째 칸에 도착하여 20만 원을 받습니다!")
                bank.deposit(player, 200000)

            # 현재 위치 정보
            current_tile = board[player.position]
            print(f"{player.name}님이 '{current_tile.name}'에 도착했습니다.")
            print(f"설명: {current_tile.description}")
            print(
                f"토지 가격: {current_tile.land_price}원, 건물 가격: {current_tile.building_prices}원"
            )

            # 다른 플레이어 소유 땅일 경우 통행료 지불
            if current_tile.owner and current_tile.owner != player:
                player.pay_toll(current_tile)

            # 황금카드 효과 적용
            if player.position in golden_cards:
                effect = golden_cards[player.position]
                print(f"🎉 황금카드 발동! {effect}")
                action = apply_special_effect(effect, player, board_length)

                # 효과에 따라 위치 이동을 반영
                if action == "move_backward":
                    steps = int(effect.split()[-1])  # 예: '뒤로 6칸 이동' -> 6
                    player.move(-steps, board_length)
                elif action == "move_forward":
                    steps = int(effect.split()[-1])  # 예: '앞으로 3칸 이동' -> 3
                    player.move(steps, board_length)
                elif action == "reroll":
                    steps = roll_dice()
                    player.move(steps, board_length)
                    print(f"{player.name}님이 주사위를 다시 굴려 {steps} 칸 이동합니다.")
                elif action == "extra_turn":
                    print(f"{player.name}님은 추가 턴을 획득했습니다!")
                    continue  # 추가 턴을 줌

                # 이동 후 새로운 위치 정보 업데이트
                current_tile = board[player.position]
                print(f"{player.name}님이 '{current_tile.name}'로 이동했습니다.")

                # 황금카드 효과 적용 후 통행료 지불 여부 확인
                if current_tile.owner and current_tile.owner != player:
                    player.pay_toll(current_tile)
                # 추가 턴 확인
                elif action == "extra_turn":
                    print(f"{player.name}님은 추가 턴을 획득했습니다!")
                    continue  # 추가 턴을 줌

                # 이동 후 새로운 위치 정보 업데이트
                current_tile = board[player.position]
                print(f"{player.name}님이 '{current_tile.name}'로 이동했습니다.")

            # 땅 구매 또는 건물 건설 선택
            if current_tile.land_price > 0:
                if current_tile.owner is None:
                    user_input = (
                        input(
                            f"{player.name}님, '{current_tile.name}'을 구매하시겠습니까? (예/아니오): "
                        )
                        .strip()
                        .lower()
                    )
                    if user_input == "예":
                        player.purchase_property(current_tile)
                elif current_tile.owner == player:
                    if current_tile.has_buildings < 3:
                        user_input = (
                            input(
                                f"{player.name}님, '{current_tile.name}'에 건물을 건설하시겠습니까? (예/아니오): "
                            )
                            .strip()
                            .lower()
                        )
                        if user_input == "예":
                            player.build_on_property(current_tile)
                    else:
                        print(
                            f"{current_tile.name}에는 더 이상 건물을 지을 수 없습니다."
                        )

                        # 부동산 판매 선택
                        if current_tile.owner == player:
                            user_input = (
                                input(
                                    f"{player.name}님, '{current_tile.name}'을 은행에 판매하시겠습니까? (예/아니오): "
                                )
                                .strip()
                                .lower()
                            )
                            if user_input == "예":
                                player.sell_property_to_bank(current_tile, bank)


if __name__ == "__main__":
    main()
