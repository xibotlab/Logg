const key = String(Math.random()).substring(2, 11);

//next
function next(id) {
    if (id == 4) {
        const adress = document.getElementById(`input1`).value;
        const nickname = document.getElementById("input2").value;
        const pw = document.getElementById("input3").value;
        const pwagain = document.getElementById("input4").value;

        if (pw == pwagain) {
            //DOM 관리
            document.getElementById('root').hidden = true;
            document.getElementById("email").hidden = false;

            //인증번호 발송
            fetch("/signup/verify", {
                method: "POST",
                body: JSON.stringify({
                    adress: adress,
                    nickname: nickname,
                    key: key
                })
            })
        } else {
            alert("다시 입력한 비밀번호가 지정한 비밀번호와 같지 않습니다.\n비밀번호를 다시 확인해주세요.")
        }
    } else if (id < 4) {
        document.getElementById("div" + id).hidden = true;
        document.getElementById("div" + String(Number(id) + 1)).hidden = false;
    }
}

//submit event function
function checkBlank(value) {
    if (value.trim().length == 0) {
        return true;
    }
    else {
        return false;
    }
}

function submit() {
    //variables
    const email = document.getElementById("input1").value
    const nickname = document.getElementById("input2").value
    const pw = document.getElementById("input3").value
    const verify = document.getElementById("verify").value

    //이상 감지
    if (checkBlank(email) || checkBlank(nickname) || checkBlank(pw)) {
        //check blank
        alert("값을 올바르게 입력하였는지 확인해주세요.");
        return false;
    }
    
    fetch("/signup/upload", {
        method: "POST",
        body: JSON.stringify({
            email: email,
            password: pw,
            username: nickname,
            key: key,
            verify: verify
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status == 405) {
            alert("인증번호가 올바르지 않습니다.")
        } else {
            alert("회원가입에 성공하였습니다.\n로그인해주세요.")
            //location.href = "login"  
        }
    })
}