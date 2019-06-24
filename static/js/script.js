document.getElementById("search_input").addEventListener('keyup', () => {
    var req = new XMLHttpRequest();
    const data = new FormData()
    req.open('POST', '/search', true);
    data.append('search_value', document.getElementById('search_input').value)
    req.onload = () => {
        var child = document.getElementById("search-response");
        if (req.status !== 200) {
            while (child.firstChild) {
                child.removeChild(child.firstChild);
            }
            console.log("Coś poszło nie tak :(");
        } else {
            while (child.firstChild) {
                child.removeChild(child.firstChild);
            }
            json_response = JSON.parse(req.responseText)
            if (json_response.length > 0) {
                if (json_response[0]["error"] != undefined) {
                    addCommunicate("Wpisz wartość w pole wyszukiwania");
                } else {
                    for (val in json_response) {
                        var container = document.createElement("DIV");
                        container.innerHTML = json_response[val]["name"];
                        container.classList.add("search-result");
                        document.getElementById("search-response").appendChild(container);
                    }
                }
            } else {
                addCommunicate("Brak wyniku");
            }

        }
    };
    req.send(data);
})

let addCommunicate = (msg) => {
    var child = document.getElementById("search-response");
    var container = document.createElement("DIV");
    container.innerHTML = msg;
    container.classList.add("search-result", "alert");
    document.getElementById("search-response").appendChild(container);
    setTimeout(function () {
        while (child.firstChild) {
            child.removeChild(child.firstChild);
        }
    }, 1750);
}

