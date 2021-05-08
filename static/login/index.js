//func
function login() {
    //get Input Value
    const email = document.getElementById("email").value.trim();
    const pw = document.getElementById("pw").value.trim();

    //send a request
    fetch("/api/login/", {
        method: "POST",
        body: JSON.stringify({
            email: email,
            pw: pw
        })
    })
    .then(res => res.json())
    .then(data => {
        const status = data.status;

        if (status == 404) {
            popup.open("계정이 존재하지 않습니다.<br>아이디를 확인해주세요.");
        } else if (status == 403) {
            popup.open("비밀번호가 올바르지 않습니다.<br>다시 시도해주세요.");
        } else if (status == 200) {
            location.href = "/"
        }
    })
}