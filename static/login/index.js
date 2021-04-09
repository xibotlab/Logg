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

        switch (status) {
            case 404:
                alert("계정이 존재하지 않습니다.\n이메일을 다시 확인해주세요.");
                break;
            case 403:
                alert("비밀번호가 알맞지 않습니다.\n비밀번호를 다시 확인해주세요.");
                break;
            case 200:
                location.href = "/"
                break;
        }
    })
}