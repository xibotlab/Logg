const form = JSON.parse($("#meta").data().form.replace(/'/g, '"'))

function checkBlank(value) {
    if (value.trim().length == 0) {
        return true;
    }
    else {
        return false;
    }
}

//next
function next(id) {
    if (id == 3) {
        //이메일 인증
        const email = $("#emailinput").val();
        const nickname = $("#nicknameinput").val();
        const pw = $("#pwinput").val();
        const pwagain = $("#pwagaininput").val()

        if (pw == pwagain) {
            //DOM 관리
            $("#root").hide();
            $("#verify").show()

            //인증번호 발송
            fetch("/api/signup/verify/", {
                method: "POST",
                body: JSON.stringify({
                    adress: email,
                    nickname: nickname
                })
            })
        } else {
            popup.open("다시 입력한 비밀번호가 올바르지 않습니다.<br>다시 확인해주세요.")
        }
    } else if (id < 4 && $(`${form[id]["id"]}input`).val() !== "") {
        //페이지 넘어가기
        document.getElementById(form[Number(id)]["id"]).hidden = true;
        document.getElementById(form[Number(id) + 1]["id"]).hidden = false;
    }
}

//가입하기
function submit() {
    //variables
    const email = $("#emailinput").val();
    const nickname = $("#nicknameinput").val()
    const pw = $("#pwinput").val()
    const verify = $("#verifynum").val()

    //이상 감지
    if (checkBlank(email) || checkBlank(nickname) || checkBlank(pw)) {
        //check blank
        popup.open("모든 입력칸에 값을 입력해주세요.");
        return false;
    }
    
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
            alert("회원가입에 성공하였습니다.\n로그인해주세요.");
            location.href = "/login/";
        }
    })
}