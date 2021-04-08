//next
function next(id) {
    if (id == 3) {
        //이메일 인증
        const adress = document.getElementById(`input0`).value;
        const nickname = document.getElementById("input1").value;
        const pw = document.getElementById("input2").value;
        const pwagain = document.getElementById("input3").value;

        if (pw == pwagain) {
            //DOM 관리
            document.getElementById('root').hidden = true;
            document.getElementById("email").hidden = false;

            //인증번호 발송
            fetch("/api/signup/verify/", {
                method: "POST",
                body: JSON.stringify({
                    adress: adress,
                    nickname: nickname
                })
            })
        } else {
            alert("다시 입력한 비밀번호가 지정한 비밀번호와 같지 않습니다.\n비밀번호를 다시 확인해주세요.")
        }
    } else if (id < 4 && document.getElementById(`input${id}`).value.trim() !== "") {
        //페이지 넘어가기
        document.getElementById("div" + id).hidden = true;
        document.getElementById("div" + String(Number(id) + 1)).hidden = false;
    }
}

function checkBlank(value) {
    if (value.trim().length == 0) {
        return true;
    }
    else {
        return false;
    }
}

//가입하기
function submit() {
    //variables
    const email = document.getElementById("input0").value
    const nickname = document.getElementById("input1").value
    const pw = document.getElementById("input2").value
    const verify = document.getElementById("verify").value

    //이상 감지
    if (checkBlank(email) || checkBlank(nickname) || checkBlank(pw)) {
        //check blank
        alert("값을 올바르게 입력하였는지 확인해주세요.");
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
            alert("인증번호가 올바르지 않습니다.\n다시 확인해주세요.")
        } else if (data == "emailerror") {
            alert("이미 존재하는 이메일입니다.\n다른 이메일로 다시 시도해주세요.")
            location.reload()
        } else {
            // alert("회원가입에 성공하였습니다.\n로그인해주세요.");
            // location.href = "login";
        }
    })
}