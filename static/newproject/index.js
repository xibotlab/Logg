document.getElementById("submit").addEventListener("click", () => {
    //element 가져오기
    const name = document.getElementById("name").value;
    const desc = document.getElementById("desc").value;

    //공백 확인
    if (name.trim() == "" || desc.trim() == "") {
        popup.open("프로젝트 이름과 설명은 필수입니다.<br>올바른 값을 입력해주세요.")
    } else {
        fetch("/api/new/", {
            method: "POST",
            body: JSON.stringify({
                name: name,
                desc: desc
            })
        })
    }
})