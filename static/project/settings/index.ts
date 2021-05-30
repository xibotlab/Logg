import { popup } from "../../api";

const idx:number = Number(document.getElementById("param")?.dataset.idx);

const category:{category: Array<string>, select: Function, selected: Number} = {
    category: eval(document.getElementById("param")?.dataset.category!),
    select: (id:number) => {
        document.getElementById(`category${category.selected}`)?.setAttribute("class", "category");
        document.getElementById(`category${id}`)?.setAttribute("class", "category select");

        document.getElementById(`page${category.selected}`)!.hidden = true;
        document.getElementById(`page${id}`)!.hidden = false;

        category.selected = id;
    },
    selected: 0
}
for (let i:number=0; i<category.category.length; i++) {
    document.getElementById(`category${i}`)?.addEventListener("click", () => {
        category.select(i);
    })
}
category.select(0);

// 메인 페이지 변경 이벤트
document.getElementById("name")?.addEventListener("change", () => {
    const name:string = (<HTMLInputElement>document.getElementById("name"))?.value;

    fetch("/api/project/update/name/", {
        method: "POST",
        body: JSON.stringify({
            idx: idx,
            name: name
        })
    })
})

document.getElementById("desc")?.addEventListener("change", () => {
    const desc:string = (<HTMLInputElement>document.getElementById("desc"))?.value;

    fetch("/api/project/update/desc/", {
        method: "POST",
        body: JSON.stringify({
            idx: idx,
            desc: desc
        })
    })
})