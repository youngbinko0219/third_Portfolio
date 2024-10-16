# import pygame
# import math
# import os
# from tiles import tile_names  # tiles.py의 tile_names 참조

# # 기본 설정
# SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
# TILE_COUNT = 36  # 타일 개수
# INNER_RADIUS = 150  # 도넛 모양의 안쪽 반지름
# OUTER_RADIUS = 250  # 도넛 모양의 바깥쪽 반지름
# DIVIDER_RATIO = 0.3  # 안쪽과 바깥쪽을 구분하는 비율 (3:7 비율)

# # 색상
# BACKGROUND_COLOR = (250, 250, 250)
# DIVIDER_COLOR = (100, 100, 100)  # 구분선 색상
# BORDER_COLOR = (0, 0, 0)  # 타일 경계 색상
# PLAYER_COLORS = [
#     (255, 0, 0),
#     (0, 255, 0),
#     (0, 0, 255),
#     (255, 255, 0),
# ]  # 각 플레이어의 색상 (예: 빨강, 초록, 파랑, 노랑)

# # pygame 초기화
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Board Game")

# # 한글 폰트 설정 (나눔고딕 폰트 파일 경로 지정)
# font_path = "NanumGothic.ttf"  # 나눔고딕 폰트 파일 경로
# if not os.path.exists(font_path):
#     print("경고: 나눔고딕 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
#     font = pygame.font.SysFont("malgungothic", 15)  # 시스템에 있는 폰트로 대체
# else:
#     font = pygame.font.Font(font_path, 15)  # 나눔고딕 폰트 사용 (텍스트 크기 조정)


# # HSV 색상을 RGB로 변환하는 함수
# def hsv_to_rgb(h, s, v):
#     color = pygame.Color(0)  # 임시 Color 객체 생성
#     color.hsva = (h, s * 100, v * 100)  # HSV 값 설정 (s와 v는 0-100 범위로 변환)
#     return color.r, color.g, color.b  # RGB 값 반환


# # 도넛 모양 타일 그리기 함수
# def draw_donut_board():
#     for i in range(TILE_COUNT):
#         angle = (2 * math.pi / TILE_COUNT) * i  # 타일 시작 각도
#         next_angle = (2 * math.pi / TILE_COUNT) * (i + 1)  # 다음 타일의 시작 각도

#         # 색상 설정: 각 타일의 고유 색상 생성 (각도에 따라 색상 변화)
#         hue = (
#             i * 360 / TILE_COUNT
#         ) % 360  # 360도를 TILE_COUNT로 나눠 각 타일에 고유 색상
#         outer_color = hsv_to_rgb(hue, 1, 1)  # 밝고 선명한 색상
#         inner_color = hsv_to_rgb((hue + 180) % 360, 1, 1)  # 보색 계산

#         # 안쪽 구획 좌표
#         inner_start = (
#             SCREEN_WIDTH // 2 + math.cos(angle) * INNER_RADIUS,
#             SCREEN_HEIGHT // 2 + math.sin(angle) * INNER_RADIUS,
#         )
#         inner_end = (
#             SCREEN_WIDTH // 2 + math.cos(next_angle) * INNER_RADIUS,
#             SCREEN_HEIGHT // 2 + math.sin(next_angle) * INNER_RADIUS,
#         )
#         divider_start = (
#             SCREEN_WIDTH // 2
#             + math.cos(angle)
#             * (INNER_RADIUS + DIVIDER_RATIO * (OUTER_RADIUS - INNER_RADIUS)),
#             SCREEN_HEIGHT // 2
#             + math.sin(angle)
#             * (INNER_RADIUS + DIVIDER_RATIO * (OUTER_RADIUS - INNER_RADIUS)),
#         )
#         divider_end = (
#             SCREEN_WIDTH // 2
#             + math.cos(next_angle)
#             * (INNER_RADIUS + DIVIDER_RATIO * (OUTER_RADIUS - INNER_RADIUS)),
#             SCREEN_HEIGHT // 2
#             + math.sin(next_angle)
#             * (INNER_RADIUS + DIVIDER_RATIO * (OUTER_RADIUS - INNER_RADIUS)),
#         )

#         # 바깥 구획 좌표
#         outer_start = (
#             SCREEN_WIDTH // 2 + math.cos(angle) * OUTER_RADIUS,
#             SCREEN_HEIGHT // 2 + math.sin(angle) * OUTER_RADIUS,
#         )
#         outer_end = (
#             SCREEN_WIDTH // 2 + math.cos(next_angle) * OUTER_RADIUS,
#             SCREEN_HEIGHT // 2 + math.sin(next_angle) * OUTER_RADIUS,
#         )

#         # 안쪽 타일 (사다리꼴) 그리기
#         inner_trapezoid_points = [inner_start, inner_end, divider_end, divider_start]
#         pygame.draw.polygon(screen, inner_color, inner_trapezoid_points)

#         # 바깥 타일 (사다리꼴) 그리기
#         outer_trapezoid_points = [divider_start, divider_end, outer_end, outer_start]
#         pygame.draw.polygon(screen, outer_color, outer_trapezoid_points)

#         # 타일 경계 그리기
#         pygame.draw.lines(screen, BORDER_COLOR, True, inner_trapezoid_points, 2)
#         pygame.draw.lines(screen, BORDER_COLOR, True, outer_trapezoid_points, 2)

#         # 타일 이름 텍스트 표시
#         text_angle = (angle + next_angle) / 2  # 텍스트 중앙 위치 각도
#         text_x = SCREEN_WIDTH // 2 + math.cos(text_angle) * (
#             INNER_RADIUS + DIVIDER_RATIO * (OUTER_RADIUS - INNER_RADIUS) / 2
#         )
#         text_y = SCREEN_HEIGHT // 2 + math.sin(text_angle) * (
#             INNER_RADIUS + DIVIDER_RATIO * (OUTER_RADIUS - INNER_RADIUS) / 2
#         )

#         # 타일 이름을 가져와 텍스트로 표시 (텍스트 색상은 바깥 타일 색상)
#         tile_name = tile_names[i % len(tile_names)]  # 타일 이름이 부족할 경우 반복
#         text_surface = font.render(tile_name, True, outer_color)
#         text_rect = text_surface.get_rect(center=(text_x, text_y))
#         screen.blit(text_surface, text_rect)


# # 플레이어 위치와 금액 표시
# # 플레이어 위치와 금액 표시
# def draw_players(players):
#     for i, player in enumerate(players):
#         # 플레이어의 위치 각도 계산
#         angle = (2 * math.pi / TILE_COUNT) * player.position

#         # 타일의 바깥 구획 내부에 위치하도록 조정
#         player_x = (
#             SCREEN_WIDTH // 2 + math.cos(angle) * (INNER_RADIUS + OUTER_RADIUS) / 2
#         )
#         player_y = (
#             SCREEN_HEIGHT // 2 + math.sin(angle) * (INNER_RADIUS + OUTER_RADIUS) / 2
#         )

#         # 플레이어 위치에 원형 아이콘 그리기
#         pygame.draw.circle(screen, PLAYER_COLORS[i], (int(player_x), int(player_y)), 10)

#         # 보드판 귀퉁이에 플레이어의 금액 표시 (한글 지원 폰트 사용)
#         cash_text = font.render(
#             f"{player.name}: ${player.cash}", True, PLAYER_COLORS[i]
#         )
#         screen.blit(cash_text, (10, 10 + i * 40))  # 40 픽셀 간격으로 배치


# # 게임 루프
# def run_visualization(players):
#     screen.fill(BACKGROUND_COLOR)
#     draw_donut_board()
#     draw_players(players)
#     pygame.display.flip()
