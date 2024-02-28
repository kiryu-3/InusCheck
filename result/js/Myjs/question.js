function checkAllRadioSelected() {
    var allRadioButtons = document.querySelectorAll('input[type="radio"]');
    var submitButton = document.getElementById("submit");
    var allSelected = true;
    var checkList = new Array(allRadioButtons.length/3); // 長さが5の配列を作成する

    for (var i = 0; i < checkList.length; i++) {
        checkList[i] = false;
    }

    for (var i = 0; i < allRadioButtons.length; i += 3) {
        for (var j = 0; j < 3; j++) {
            if (allRadioButtons[i + j].checked) {
                checkList[i / 3] = true;
                break;
            }
        }
    }

    for (var i = 0; i < checkList.length; i++) {
        if (!checkList[i]) {
            allSelected = false;
            break;
        }
    }

    if (allSelected) {
        submitButton.disabled = false; // すべてのラジオボタンが選択されていたら送信ボタンを有効にする
    } else {
        submitButton.disabled = true; // 少なくとも1つのラジオボタンが未選択の場合は送信ボタンを無効にする
    }
}

function checkRadioSelected() {
    checkAllRadioSelected(); // どれか1つのラジオボタンが選択されたら全体をチェック
}