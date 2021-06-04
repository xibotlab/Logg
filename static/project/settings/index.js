const idx = Number(document.getElementById("param")?.dataset.idx);

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

// 메인 페이지 변경 이벤트
document.getElementById("name").addEventListener("change", () => {
    const name = document.getElementById("name").value;

    fetch("/api/project/update/name/", {
        method: "POST",
        body: JSON.stringify({
            idx: idx,
            name: name
        })
    })
})

document.getElementById("desc").addEventListener("change", () => {
    const desc = document.getElementById("desc").value;

    fetch("/api/project/update/desc/", {
        method: "POST",
        body: JSON.stringify({
            idx: idx,
            desc: desc
        })
    })
})