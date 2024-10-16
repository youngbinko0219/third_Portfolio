# tiles.py

from tile_descriptions import get_tile_description  # 타일 설명 함수 임포트
from properties import Property

# 인구 30만 이상의 도시 목록
tile_names = [
    "서울",
    "인천",
    "수원",
    "고양",
    "용인",
    "성남",
    "부천",
    "안산",
    "화성",
    "남양주",
    "의정부",
    "시흥",
    "파주",
    "김포",
    "광명",
    "대전",
    "청주",
    "천안",
    "아산",
    "광주",
    "전주",
    "부산",
    "대구",
    "울산",
    "창원",
    "김해",
    "진주",
    "포항",
    "춘천",
    "평양",
    "남포",
    "함흥",
    "청진",
    "신의주",
    "해주",
    "평택",
]

# 각 도시의 토지 가격과 첫 번째 건물 가격 설정
tile_prices = {
    "서울": {"land_price": 600000, "building_price": 250000},
    "부산": {"land_price": 500000, "building_price": 200000},
    "인천": {"land_price": 450000, "building_price": 180000},
    "대구": {"land_price": 400000, "building_price": 160000},
    "대전": {"land_price": 350000, "building_price": 140000},
    "광주": {"land_price": 300000, "building_price": 120000},
    "수원": {"land_price": 400000, "building_price": 160000},  # 7
    # 인구 50만 ~ 100만 도시
    "고양": {"land_price": 350000, "building_price": 140000},
    "용인": {"land_price": 340000, "building_price": 136000},
    "성남": {"land_price": 330000, "building_price": 132000},
    "부천": {"land_price": 320000, "building_price": 128000},
    "안산": {"land_price": 310000, "building_price": 124000},
    "화성": {"land_price": 300000, "building_price": 120000},
    "남양주": {"land_price": 290000, "building_price": 116000},
    "평양": {"land_price": 500000, "building_price": 200000},
    "울산": {"land_price": 370000, "building_price": 148000},
    "창원": {"land_price": 360000, "building_price": 144000},  # 10
    # 인구 30만 ~ 50만 도시
    "천안": {"land_price": 280000, "building_price": 112000},
    "아산": {"land_price": 270000, "building_price": 108000},
    "청주": {"land_price": 260000, "building_price": 104000},
    "전주": {"land_price": 250000, "building_price": 100000},
    "의정부": {"land_price": 240000, "building_price": 96000},
    "시흥": {"land_price": 230000, "building_price": 92000},
    "파주": {"land_price": 220000, "building_price": 88000},
    "김포": {"land_price": 210000, "building_price": 84000},
    "광명": {"land_price": 200000, "building_price": 80000},
    "남포": {"land_price": 250000, "building_price": 100000},
    "함흥": {"land_price": 240000, "building_price": 96000},
    "청진": {"land_price": 230000, "building_price": 92000},
    "신의주": {"land_price": 220000, "building_price": 88000},
    "해주": {"land_price": 200000, "building_price": 80000},
    "춘천": {"land_price": 210000, "building_price": 84000},
    "진주": {"land_price": 200000, "building_price": 80000},
    "김해": {"land_price": 250000, "building_price": 100000},
    "포항": {"land_price": 240000, "building_price": 96000},
    "평택": {"land_price": 190000, "building_price": 76000},
}


def create_tiles():
    tiles = []
    for name in tile_names:
        description = get_tile_description(name)
        land_price = tile_prices[name]["land_price"]
        building_price = tile_prices[name]["building_price"]
        building_prices = [
            building_price,  # 첫 번째 건물 가격
            building_price * 2,  # 두 번째 건물 가격
            building_price * 4,  # 세 번째 건물 가격
        ]
        # Property 객체로 타일 생성
        property_tile = Property(name, land_price, building_prices)
        property_tile.description = description  # 설명 추가
        tiles.append(property_tile)
    return tiles
