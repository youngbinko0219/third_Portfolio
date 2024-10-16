# properties.py


class Property:
    def __init__(self, name, land_price, building_prices):
        self.name = name
        self.land_price = land_price
        self.building_prices = building_prices  # 최대 3채 건물 가격 리스트
        self.owner = None
        self.has_buildings = 0  # 지어진 건물 수

    def purchase_land(self, player):
        """
        토지를 구매하고 소유자를 설정합니다.
        """
        if self.owner is None:
            player.cash -= self.land_price
            self.owner = player
            return True
        return False

    def build(self, player):
        """
        건물을 최대 3채까지 건설합니다. 각 건물 가격은 리스트의 순서대로 적용됩니다.
        """
        if self.owner == player and self.has_buildings < 3:  # 최대 3채까지만 건설 가능
            build_cost = self.building_prices[self.has_buildings]
            if player.cash >= build_cost:
                player.cash -= build_cost
                self.has_buildings += 1
                print(
                    f"{player.name}님이 {self.name}에 건물 {self.has_buildings}채를 건설했습니다."
                )
                return True
            else:
                print(
                    f"{player.name}님은 {self.name}에 건물을 건설할 충분한 현금이 없습니다."
                )
        else:
            print(f"{self.name}에는 더 이상 건물을 건설할 수 없습니다.")
        return False

    def calculate_property_value(self):
        """
        토지와 지어진 건물들의 총 가치를 반환합니다.
        """
        total_value = self.land_price
        for i in range(self.has_buildings):
            total_value += self.building_prices[i]
        return total_value

    def calculate_toll(self):
        """
        통행료를 계산합니다. 토지 가격 + 각 건물 가격의 20%를 더한 값으로 설정합니다.
        """
        toll = self.land_price * 0.2  # 기본 토지 가격의 20%
        for i in range(self.has_buildings):
            toll += self.building_prices[i] * 0.2  # 각 건물 가격의 20%
        return int(toll)
