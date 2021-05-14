document.getElementById("name").addEventListener("change", () => {
    const idx = $("#project").data().idx;
    const name = $("#name").val();

    fetch("/api/project/update/name/", {
        method: "POST",
        body: JSON.stringify({
            idx: idx,
            name: name
        })
    })
})