const popup = {
    open: (value) => {
        document.getElementById("pop").hidden = false;
        document.getElementById("popvalue").innerHTML = value;
    },
    close: () => {
        document.getElementById("pop").hidden = true;
    }
}