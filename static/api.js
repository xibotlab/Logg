const popup = {
    open: function(value) {
        document.getElementById("pop").hidden = false;
        document.getElementById("popvalue").innerHTML = value;
    },
    close: function() {
        document.getElementById("pop").hidden = true;
    }
}