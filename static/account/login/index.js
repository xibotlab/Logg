document.getElementById("submit").addEventListener("click", () => {
    const email = document.getElementById("email").value.trim();
    const pw = document.getElementById("pw").value.trim();

    if (email == "" || pw == "") {
        popup.open("모든 필드에 값을 입력해주세요.");
        return null;
    }

    fetch("/api/login/", {
        method: "POST",
        body: JSON.stringify({
            email: email,
            pw: pw
        })
    })
    .then(res => res.json())
    .then(data => {
        const status = Number(data.status);

        switch(status) {
            case 404:
                popup.open("아이디가 존재하지 않습니다.\n아이디 확인 후 다시 시도해주세요.");
                break;
            case 403:
                popup.open("비밀번호가 올바르지 않습니다.\n비밀번호 확인 후 다시 시도해주세요.");
                break;
            case 200:
                location.href = "/";
        }
    })
})