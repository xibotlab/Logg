document.getElementById("name").addEventListener("change", () => {
    const idx = Number(document.getElementById("project")?.dataset.idx);
    const name = document.getElementById("name").value;

    fetch("/api/project/update/name/", {
        method: "POST",
        body: JSON.stringify({
            idx: idx,
            name: name
        })
    })
}) 