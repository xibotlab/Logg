//DOM 설정
const data = [
    {
        title: "이메일",
        type: "text",
        placeholder: "이메일을 입력해주세요..."
    },
    {
        title: "닉네임",
        type: "text",
        placeholder: "실명을 입력하지 마세요."
    },
    {
        title: "비밀번호",
        type: "password",
        placeholder: "아무에게도 알려주지 마세요."
    },
    {
        title: "비밀번호 재입력",
        type: "password",
        placeholder: "다시 비밀번호를 입력합니다."
    }
]

for (let i=0; i<4; i++) {
    //메인 div
    const div = document.createElement("div");
    div.style.textAlign = "center";
    div.setAttribute("id", `div${i}`)
    div.setAttribute("hidden", true);
    document.getElementById("root").appendChild(div);   

    //메인 타이틀
    const h1 = document.createElement("h1");
    h1.style.fontSize = "2rem";
    h1.style.marginBottom = "1px";
    h1.innerText = data[i]["title"];
    div.appendChild(h1);

    //input
    const input = document.createElement("input");
    input.setAttribute("type", data[i]["type"])
    input.setAttribute("id", `input${i}`)
    input.setAttribute("placeholder", data[i]["placeholder"])
    input.style.marginBottom = "1vh";
    input.style.width = "240px";
    div.appendChild(input);
    div.appendChild(document.createElement("br")); //br태그

    //button
    const button = document.createElement("button");
    button.onclick = () => {
        next(i)
    }
    button.innerText = "확인"
    div.appendChild(button);
}

document.getElementById("div0").removeAttribute("hidden")