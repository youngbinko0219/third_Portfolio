$(document).ready(function () {
  const playerPositions = [0, 0, 0, 0]; // 모든 플레이어의 초기 위치는 0
  const playerColors = ["red", "blue", "green", "yellow"]; // 각 플레이어의 말 색상

  // 10x10 보드에서 가장자리에만 타일 번호를 배치하는 배열 (1~36)
  const tileNumbers = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    36,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    11,
    35,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    12,
    34,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    13,
    33,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    14,
    32,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    15,
    31,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    16,
    30,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    17,
    29,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null,
    18,
    28,
    27,
    26,
    25,
    24,
    23,
    22,
    21,
    20,
    19,
  ];

  // 타일을 생성하며 가장자리에만 숫자를 넣고, 중앙 부분은 빈칸으로 둡니다.
  let tileIndex = 0;

  for (let i = 0; i < 10; i++) {
    for (let j = 0; j < 10; j++) {
      const tileNumber = tileNumbers[tileIndex];
      if (tileNumber !== null) {
        $("#board").append(
          `<div class="tile" id="tile-${tileIndex}">${tileNumber}</div>`
        );
      } else {
        $("#board").append(`<div class="tile empty"></div>`);
      }
      tileIndex++;
    }
  }

  // 주사위 굴리기 및 플레이어 이동 함수
  function movePlayer(playerId, newPosition) {
    $(`#tile-${playerPositions[playerId]}`)
      .find(`.player-${playerId}`)
      .remove();
    playerPositions[playerId] = newPosition;
    $(`#tile-${newPosition}`).append(
      `<div class="player-piece player-${playerId}" style="background-color: ${playerColors[playerId]};"></div>`
    );
  }

  $("#roll-dice-button").click(function () {
    // 주사위 애니메이션 시작
    $("#dice-result").addClass("rolling");

    // 1초 후에 주사위 결과 계산 및 표시
    setTimeout(() => {
      const playerId = $("#player-select").val();
      $.post("/roll_dice", { player_id: playerId }, function (data) {
        let message = `${data.player}님이 ${data.position} 위치에 도착했습니다.<br>`;
        message += `현재 위치: ${data.tile}<br>`;
        message += `설명: ${data.description}<br>`;
        message += `잔고: ${data.cash}원<br>`;
        if (data.steps !== undefined) {
          message += `<strong>주사위: ${data.steps}</strong><br>`; // 주사위 결과 표시
        }
        if (data.message) {
          message += `<strong>${data.message}</strong>`;
        }
        $("#player-info").html(message);
        $(".actions").show(); // 액션 버튼 표시

        // 주사위 결과 표시 및 애니메이션 제거
        $("#dice-result").text(`🎲 ${data.steps}`); // 주사위 결과 표시
        $("#dice-result").removeClass("rolling"); // 애니메이션 제거

        // 플레이어 위치 업데이트
        movePlayer(playerId, data.position);
      }).fail(function () {
        alert("서버와의 통신 중 오류가 발생했습니다.");
      });
    }, 1000); // 1초 대기 후 결과 처리
  });

  // 땅 구매, 건물 건설, 땅 판매 버튼 클릭 이벤트
  $("#buy-property-button").click(function () {
    sendAction("buy_property");
  });
  $("#build-property-button").click(function () {
    sendAction("build_property");
  });
  $("#sell-property-button").click(function () {
    sendAction("sell_property");
  });

  // 선택한 액션을 서버에 전달
  function sendAction(actionType) {
    const playerId = $("#player-select").val();
    $.post(
      "/take_action",
      { player_id: playerId, action: actionType },
      function (data) {
        let message = `${data.player}님이 ${data.position} 위치에 도착했습니다.<br>`;
        message += `현재 위치: ${data.tile}<br>`;
        message += `설명: ${data.description}<br>`;
        message += `잔고: ${data.cash}원<br>`;
        if (data.message) {
          message += `<strong>${data.message}</strong>`;
        }
        $("#player-info").html(message);
        $(".actions").hide(); // 액션 버튼 숨기기

        // 땅 구매 후 타일 색상 변경
        if (actionType === "buy_property" && data.tile) {
          const tileNumber = data.position; // 위치 정보
          $(`#tile-${tileNumber}`).css(
            "background-color",
            playerColors[playerId]
          );
        }
      }
    ).fail(function () {
      alert("서버와의 통신 중 오류가 발생했습니다.");
    });
  }
});
