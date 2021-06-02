const form = JSON.parse(document.getElementById("form").dataset.form.replace(/'/g, '"'))

function CheckBlank(value) {
    if (value.trim().length == 0) {
        return true;
    }
    else {
        return false;
    }
}

for (let idx=0; idx<form.length; idx++) {
    document.getElementById(`btn${idx}`).addEventListener("click", () => {
        if (idx == form.length-1) {
            const email = document.getElementById("emailinput").value;
            const nickname = document.getElementById("nicknameinput").value;
            const pw = document.getElementById("pwinput").value;
            const pwagain = document.getElementById("pwagaininput").value;

            if (pw == pwagain) {
                document.getElementById("root").hidden = true;
                document.getElementById("verify").hidden = false;

                fetch("/api/signup/verify/", {
                    method: "POST",
                    body: JSON.stringify({
                        adress: email,
                        nickname: nickname
                    })
                })
            } else {
                popup.open("비밀번호가 같지 않습니다.\n다시 입력해주세요.")
            }
        } else {
            document.getElementById(form[idx]["id"]).hidden = true;
            document.getElementById(form[idx+1]["id"]).hidden = false;
        }
    })
}

//가입하기
document.getElementById("verifybtn")?.addEventListener("click", () => {
    const email = document.getElementById("emailinput").value;
    const nickname = document.getElementById("nicknameinput").value;
    const pw = document.getElementById("pwinput").value;
    const verify = document.getElementById("verifynum").value;

    fetch("/api/signup/", {
        method: "POST",
        body: JSON.stringify({
            email: email,
            password: pw,
            username: nickname,
            verify: verify
        })
    })
    .then(res => res.text())
    .then(result => {
        const data = result.trim()
        
        if (data == "verifyerror") {
            popup.open("인증번호가 올바르지 않습니다.<br>다시 확인해주세요.")
        } else if (data == "emailerror") {
            popup.open("이미 존재하는 이메일입니다.<br>다른 이메일로 다시 시도해주세요.")
            location.reload()
        } else {
            location.href = "/login/";
        }
    })
})