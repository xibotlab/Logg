const idx = Number(document.getElementById("param")?.dataset.idx);

//카테고리 관련 코드
const category = {
    category: eval(document.getElementById("param").dataset.category),
    select: (id) => {
        document.getElementById(`category${category.selected}`)?.setAttribute("class", "category");
        document.getElementById(`category${id}`)?.setAttribute("class", "category select");

        document.getElementById(`page${category.selected}`).hidden = true;
        document.getElementById(`page${id}`).hidden = false;

        category.selected = id;
    },
    selected: 0
}
for (let i=0; i<category.category.length; i++) {
    document.getElementById(`category${i}`)?.addEventListener("click", () => {
        category.select(i);
    })
}
category.select(0);

// // 메인 페이지 변경 이벤트
// function UpdateEvent({url, id, value}) {

// }

document.getElementById("name").addEventListener("change", () => {
    fetch(`/api/project/update/name/${idx}/`, {
        method: "POST",
        body: JSON.stringify({
            name: document.getElementById("name").value
        })
    })
})

document.getElementById("desc").addEventListener("change", () => {
    fetch(`/api/project/update/desc/${idx}/`, {
        method: "POST",
        body: JSON.stringify({
            desc: document.getElementById("desc").value
        })
    })
})

//트리 생성
function newTree() {
    fetch(`/api/project/new/tree/${idx}/`, {
        method: "POST",
        body: JSON.stringify({
            name: document.getElementById("newTreeName").value
        })
    })
}