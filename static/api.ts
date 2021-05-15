const popup = {
    open: (value:string) => {
        document.getElementById("pop")!.hidden = false;
        (<HTMLInputElement>document.getElementById("popvalue")).innerHTML = value;
    },
    close: () => {
        document.getElementById("pop")!.hidden = true;
    }
}

document.getElementById("popclose")?.addEventListener("click", () => {
    popup.close();
})

export { popup }