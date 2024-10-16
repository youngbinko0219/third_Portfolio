# bank.py


class Bank:
    def deposit(self, player, amount):
        """
        플레이어의 현금에 단순히 입금합니다.
        """
        player.cash += amount
        print(
            f"{player.name}님의 현금이 {amount}원 증가하여 총 {player.cash}원이 되었습니다."
        )

    def withdraw(self, player, amount):
        """
        플레이어가 은행에서 현금을 출금합니다. 현금이 부족하면 False를 반환합니다.
        """
        if player.cash >= amount:
            player.cash -= amount
            print(
                f"{player.name}님의 현금이 {amount}원 감소하여 총 {player.cash}원이 되었습니다."
            )
            return True
        else:
            print(f"{player.name}님의 현금이 부족하여 {amount}원을 출금할 수 없습니다.")
            return False
