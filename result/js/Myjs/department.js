var universityDropdown = document.getElementById("university");
var gradeDropdown = document.getElementById("grade");
var courseDropdown = document.getElementById("course");

// 大学名のドロップダウンを設定
for (var university in universityData) {
    var option = document.createElement("option");
    console.log(universityDropdown);
    option.value = university;
    option.text = university;
    universityDropdown.add(option);
}

// 大学名が選択された時の処理
function updateDepartments() {
    // 学年と所属のドロップダウンをクリア
    gradeDropdown.length = 1;
    courseDropdown.length = 1;

    var selectedUniversity = universityDropdown.value;
    if (selectedUniversity in universityData) {
        var grades = Object.keys(universityData[selectedUniversity]);

        // 学年のドロップダウンを設定
        for (var i = 0; i < grades.length; i++) {
            var option = document.createElement("option");
            option.value = grades[i];
            option.text = grades[i];
            gradeDropdown.add(option);
        }
    }
}

// 学年が選択された時の処理
function updateCourses() {
    // 所属のドロップダウンをクリア
    courseDropdown.length = 1;

    var selectedUniversity = universityDropdown.value;
    var selectedGrade = gradeDropdown.value;
    
    if (selectedUniversity in universityData && selectedGrade in universityData[selectedUniversity]) {
        var courses = universityData[selectedUniversity][selectedGrade];

        // 所属のドロップダウンを設定
        for (var i = 0; i < courses.length; i++) {
            var option = document.createElement("option");
            option.value = courses[i];
            option.text = courses[i];
            courseDropdown.add(option);
        }
    }
}

// ページ読み込み後に実行
window.onload = function() {
    // 20秒後にボタンを有効にする
    setTimeout(function() {
        isButtonEnabled = true;
        checkButtonState();
    }, 30000);
};

function validateForm() {
    // セレクトボックスの値が空の場合は送信をキャンセル
    var university = document.getElementById('university').value;
    var grade = document.getElementById('grade').value;
    var course = document.getElementById('course').value;

    if (university === '' || grade === '' || course === '') {
        alert('大学名、学年、所属を選択してください');
        return false;
    }

    return true;
}

function checkButtonState() {
    // ボタンが有効で、かつ全てのセレクトボックスが選択された場合にボタンを有効にする
    if (isButtonEnabled) {
        var university = document.getElementById('university').value;
        var grade = document.getElementById('grade').value;
        var course = document.getElementById('course').value;

        if (university !== '' && grade !== '' && course !== '') {
            document.getElementById('startButton').disabled = false;
        }
    }
}

// セレクトボックスの変更時にボタンの状態をチェック
document.getElementById('university').addEventListener('change', checkButtonState);
document.getElementById('grade').addEventListener('change', checkButtonState);
document.getElementById('course').addEventListener('change', checkButtonState);