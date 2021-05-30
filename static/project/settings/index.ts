const category:{category: Array<string>, select: Function, selected: Number} = {
    category: eval(document.getElementById("param")?.dataset.category!),
    select: (id:number) => {
        document.getElementById(`category${category.selected}`)?.setAttribute("class", "category");
        document.getElementById(`category${id}`)?.setAttribute("class", "category select");
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