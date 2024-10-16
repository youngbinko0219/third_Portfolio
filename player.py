# player.py


class Player:
    def __init__(self, name, initial_cash=1000000):
        """
        플레이어의 이름, 초기 위치, 이동 거리, 현금, 소유한 자산을 초기화합니다.
        """
        self.name = name
        self.position = 0  # 초기 위치 (보드에서 시작 위치는 0)
        self.total_distance = 0  # 총 이동 거리
        self.cash = initial_cash
        self.properties = []  # 소유한 부동산 목록

    def move(self, steps, num_tiles):
        """
        플레이어가 주사위 결과(steps)만큼 보드 위에서 전진합니다.
        순환형 보드에서 마지막 칸을 넘어가면 첫 번째 칸으로 돌아옵니다.
        steps (int): 주사위 결과로 이동할 칸 수
        num_tiles (int): 보드의 총 칸 수
        """
        self.position = (self.position + steps) % num_tiles
        self.total_distance += steps  # 총 이동 거리에 steps를 누적
        return f"{self.name} moved forward by {steps} steps to position {self.position}"

    def get_total_distance(self):
        """
        플레이어가 이동한 총 거리를 반환합니다.
        """
        return f"Total distance traveled by {self.name}: {self.total_distance} steps"

    def get_current_location(self, board, golden_cards):
        """
        현재 위치한 칸의 상세 설명을 반환합니다.
        board (list): 보드의 각 칸 정보를 담은 리스트
        golden_cards (dict): 황금카드 위치를 담은 딕셔너리, 키는 칸의 위치, 값은 황금카드의 효과 설명
        """
        current_tile = board[self.position]
        description = f"현재 위치: {current_tile['name']}\n"

        # 황금카드인지 확인
        if self.position in golden_cards:
            description += (
                f"이곳은 황금카드 칸입니다! 효과: {golden_cards[self.position]}\n"
            )
        else:
            description += "일반 칸입니다.\n"

        # 땅 소유 여부 확인
        if current_tile.get("owner") is None:
            description += "이 땅은 구매할 수 있습니다.\n"
        elif current_tile["owner"] == self:
            description += (
                "이 땅은 당신이 소유하고 있습니다. 건물을 건설할 수 있습니다.\n"
            )
        else:
            description += (
                f"이 땅은 {current_tile['owner'].name}님이 소유하고 있습니다.\n"
            )

        return description

    def purchase_property(self, property_tile):
        """
        플레이어가 토지를 구매합니다. 소유자가 없고, 현금이 충분할 때만 구매 가능합니다.
        property_tile (Property): 구매할 타일 정보
        """
        if self.cash >= property_tile.land_price and property_tile.owner is None:
            self.cash -= property_tile.land_price
            property_tile.owner = self
            self.properties.append(property_tile)
            print(f"{self.name}님이 {property_tile.name} 토지를 구매했습니다.")
            print(f"남은 현금: {self.cash}원")
        else:
            print(f"{self.name}님은 {property_tile.name} 토지를 구매할 수 없습니다.")

    def build_on_property(self, property_tile):
        """
        플레이어가 소유한 토지에 건물을 건설합니다. 이미 건물이 있는 경우 건설 불가합니다.
        property_tile (Property): 건설할 타일 정보
        """
        if property_tile.owner == self and property_tile.has_buildings < 3:
            build_cost = property_tile.building_prices[property_tile.has_buildings]
            if self.cash >= build_cost:
                self.cash -= build_cost
                property_tile.has_buildings += 1
                print(
                    f"{self.name}님이 {property_tile.name}에 건물 {property_tile.has_buildings}채를 건설했습니다."
                )
                print(f"남은 현금: {self.cash}원")
            else:
                print(
                    f"{self.name}님은 {property_tile.name}에 건물을 건설할 충분한 현금이 없습니다."
                )
        else:
            print(f"{property_tile.name}에는 더 이상 건물을 건설할 수 없습니다.")

    def calculate_total_assets(self):
        """
        플레이어의 총 자산을 계산하여 반환합니다 (현금 + 모든 부동산 가치).
        """
        total_assets = self.cash
        for property in self.properties:
            total_assets += property.calculate_property_value()
        return total_assets

    def sell_property_to_bank(self, property):
        """
        플레이어가 소유한 부동산을 은행에 판매하고, 구매 가격의 80%를 현금으로 받습니다.
        """
        if property in self.properties:
            sale_price = property.sell_to_bank()
            self.cash += sale_price
            self.properties.remove(property)
            print(
                f"{self.name}님이 {property.name}을(를) 은행에 {sale_price}원에 판매했습니다."
            )
        else:
            print(f"{self.name}님은 {property.name}을(를) 소유하고 있지 않습니다.")

    def pay_toll(self, property_tile):
        """
        다른 플레이어의 소유 땅에 도착했을 때 통행료를 지불합니다.
        현금이 부족하면 소유한 부동산을 판매하여 통행료를 충당하며, 전 재산으로도 충당하지 못할 경우 파산 처리합니다.
        """
        toll = property_tile.calculate_toll()

        # 현금 부족 시 부동산 판매로 충당
        while self.cash < toll and self.properties:
            # 소유한 부동산을 가치 기준으로 정렬하여 가장 저렴한 부동산부터 판매
            self.properties.sort(key=lambda x: x.calculate_property_value())
            cheapest_property = self.properties.pop(0)  # 가장 저렴한 부동산 선택
            sale_price = cheapest_property.sell_to_bank()
            self.cash += sale_price
            print(
                f"{self.name}님이 {cheapest_property.name}을(를) {sale_price}원에 판매했습니다."
            )

        # 통행료 지불
        if self.cash >= toll:
            self.cash -= toll
            property_tile.owner.cash += toll
            print(
                f"{self.name}님이 {property_tile.owner.name}님에게 통행료 {toll}원을 지불했습니다."
            )
            print(f"{self.name}님의 남은 현금: {self.cash}원")
        else:
            # 현금과 부동산으로도 충당하지 못하는 경우 파산 처리
            property_tile.owner.cash += self.cash  # 남은 현금을 모두 상대에게 지급
            print(
                f"{self.name}님이 {property_tile.owner.name}님에게 가진 전부 {self.cash}원을 지불했습니다."
            )
            self.cash = 0
            print(f"{self.name}님은 파산하셨습니다.")
            self.is_bankrupt = True  # 파산 상태 표시
