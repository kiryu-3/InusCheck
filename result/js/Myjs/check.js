function showQuestions() {
    var category = document.getElementById("category").value;
    for (var i = 1; i <= 66; i++) {
      var elementsq = document.getElementById("question" + i);
      var elementss = document.getElementsByClassName("skill" + i);
      console.log(elementss);

      if (category === "オンライン・コラボレーション力" && i >= 1 && i <= 15) {
        elementsq.style.display = "block";
        for (var j = 0; j < elementss.length; j++) {
          elementss[j].style.display = "block";
        }
      } else if (category === "データ利活用力" && i >= 16 && i <= 30) {
        elementsq.style.display = "block";
        for (var j = 0; j < elementss.length; j++) {
          elementss[j].style.display = "block";
        }
      } else if (category === "情報システム開発力" && i >= 31 && i <= 44) {
        elementsq.style.display = "block";
        for (var j = 0; j < elementss.length; j++) {
          elementss[j].style.display = "block";
        }
      } else if (category === "情報倫理力" && i >= 45 && i <= 66) {
        elementsq.style.display = "block";
        for (var j = 0; j < elementss.length; j++) {
          elementss[j].style.display = "block";
        }
      } else {
        elementsq.style.display = "none";
        for (var j = 0; j < elementss.length; j++) {
          elementss[j].style.display = "none";
        }
      }
    }
  }

// 大学名が選択された時の処理
function updateDepartments() {
    // 学年と所属のドロップダウンをクリア
    gradeDropdown.length = 0;
    courseDropdown.length = 0;

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
    courseDropdown.length = 0;

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