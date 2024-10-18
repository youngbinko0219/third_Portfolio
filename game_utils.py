# game_utils.py


def display_welcome_message():
    """
    게임 시작 시 환영 메시지를 출력
    """
    print("🎉 어드벤처 보드 게임에 오신 것을 환영합니다! 🎉")
    print("주사위를 굴리고 보드를 이동하세요. 끝에 도달하면 승리합니다!")
    print("현재 위치의 설명을 보려면 언제든지 'location'을 입력하세요.\n")


def calculate_remaining_distance(player_position, board_length):
    """
    플레이어가 도착점까지 남은 거리를 계산
    """
    return max(board_length - player_position - 1, 0)


def check_end_game(players):
    """
    게임 종료 조건을 확인합니다. 한 플레이어를 제외한 나머지 모든 플레이어의 현금과 부동산이 소진되면 게임 종료.
    """
    active_players = [
        player for player in players if player.cash > 0 or player.properties
    ]

    # 활성 플레이어가 1명만 남아있다면 종료 조건 충족
    if len(active_players) == 1:
        print(
            f"{active_players[0].name}님이 모든 플레이어의 자산을 없애서 승리했습니다!"
        )
        return True
    return False


def check_for_quit(player_name):
    """
    플레이어의 턴마다 게임을 멈출지 확인하는 함수. 웹에서는 항상 False를 반환하도록 수정.
    """
    # 웹 게임에서는 종료 확인 없이 자동 진행되므로 항상 False 반환
    return False
