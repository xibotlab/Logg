document.getElementById("name")?.addEventListener("change", () => {
    const idx:Number = Number(document.getElementById("project")?.dataset.idx);
    const name:String = (<HTMLInputElement>document.getElementById("name")).value;

    fetch("/api/project/update/name/", {
        method: "POST",
        body: JSON.stringify({
            idx: idx,
            name: name
        })
    })
})