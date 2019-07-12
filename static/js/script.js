// Wyświetla warości z pola wyszukiwania 
if (document.getElementById("search_input")) {
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
                            var aTag = document.createElement("a");
                            aTag.setAttribute("href", json_response[val]["name"]);
                            aTag.innerHTML = json_response[val]["name"];
                            container.appendChild(aTag);
                            container.id = "searchid";
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
}

// wyświetla komunikaty 
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

// Aktualizacja bazy danych
if (document.getElementById('update-button')) {
    document.getElementById('update-button').addEventListener("click", () => {
        var req = new XMLHttpRequest();
        req.open('POST', '/update');
        document.getElementById("loader").style.display = 'block';
        document.getElementById("content-block").style.display = 'none';
        req.onload = () => {
            document.getElementById("loader").style.display = 'none';
            document.getElementById("content-block").style.display = 'block';
        }
        req.send();

    });

}

// W zależności od wartości dodaje kolor do elementu z procentowym dziennym zwrotem z inwestycji 
if (document.getElementById('stock-change')) {
    let gain = document.getElementById('stock-change').innerHTML;
    let number = parseFloat(gain.trim().split(" ")[0].substr(1));
    if (number > 0) {
        document.getElementById('stock-change').classList.add('stock-change-up');
    } else if(number == 0) {
        document.getElementById('stock-change').classList.add('stock-change-zero');
    }else{
        document.getElementById('stock-change').classList.add('stock-change-down');
    }
}
