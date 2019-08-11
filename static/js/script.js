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

// Przekierowuje na stronę z wiadomościami
if (document.getElementById('news-button')) {
    document.getElementById('news-button').addEventListener("click", () => {
    window.location.href = "http://127.0.0.1:5000/news";
    });
}

// Przkierowuje na stronę z transakcjami
if (document.getElementById('market-button')) {
    document.getElementById('market-button').addEventListener("click", () => {
    window.location.href = "http://127.0.0.1:5000/market";
    });
}

// Przkierowuje na stronę z sygnałami bollingera
if (document.getElementById('boll-button')) {
    document.getElementById('boll-button').addEventListener("click", () => {
    document.getElementById("loader").style.display = 'block';
    document.getElementById("content-block").style.display = 'none';
    window.location.href = "http://127.0.0.1:5000/bollsignals";
    });
}

// W zależności od wartości dodaje kolor do elementu z procentowym dziennym zwrotem z inwestycji 
if (document.getElementById('stock-change')) {
    let gain = document.getElementById('stock-change').innerHTML;
    let number = parseFloat(gain.trim().split(" ")[0].substr(1));
    if (number > 0) {
        document.getElementById('stock-change').classList.add('stock-change-up');
    } else if (number == 0) {
        document.getElementById('stock-change').classList.add('stock-change-zero');
    } else {
        document.getElementById('stock-change').classList.add('stock-change-down');
    }
}

// Wyświetla wyniki analizy wolumenów
if (document.getElementById('analyze-button')) {
    document.getElementById('analyze-button').addEventListener("click", () => {
        var req = new XMLHttpRequest();
        req.open('POST', '/analyze');
        document.getElementById("loader").style.display = 'block';
        document.getElementById("content-block").style.display = 'none';
        req.onload = () => {
            document.getElementById("loader").style.display = 'none';
            document.getElementById("content-block").style.display = 'block';
            if (req.status !== 200) {
                console.log('Error');
            } else {
                response = JSON.parse(req.responseText);

                var container = document.getElementsByClassName("main-container")[0];

                var analyze_container = document.createElement('div');
                analyze_container.setAttribute('class', 'analyze-container');

                // Kontener z krzyżykiem do zamkniecia listy 
                var emptydiv = document.createElement('div');
                var analyze_container_close = document.createElement('div');
                analyze_container_close.setAttribute('class', 'analyze-container-close');
                analyze_container_close.setAttribute('id', 'close-analyze');
                analyze_container_close.innerHTML = "X";
                emptydiv.appendChild(analyze_container_close);
                // Koniec krzyżyka

                var analyze_display_container = document.createElement('div');
                analyze_display_container.setAttribute('class', 'analyze-display-container');
                analyze_display_container.appendChild(create_column(90,0));
                analyze_display_container.appendChild(create_column(30,1));
                analyze_container.appendChild(emptydiv);
                analyze_container.appendChild(analyze_display_container);
                container.appendChild(analyze_container);

                // Usuwa wyniki po naciśnięciu krzyżyka 
                document.getElementById("close-analyze").addEventListener('click', () => {
                    var parent = document.getElementsByClassName("analyze-container")[0];
                    parent.remove();
                })

            }
        }
        req.send();
    })
}

// Tworzy kolumnę z wynikami analizy
let create_column = (day, num) => {
    var analyze_display = document.createElement('div');
    analyze_display.setAttribute('class', 'analyze-display');
    var section_header = document.createElement('div');
    section_header.setAttribute('class', 'section-header');
    section_header.innerHTML = day + " dni";
    analyze_display.appendChild(section_header);
    
    for (var i = 0; i < response[num]['value'].length; i++) {
        var analyze_item = document.createElement('div');
        analyze_item.setAttribute('class', 'analyze-item');
        // Pusty div
        var item_empty_div = document.createElement('div');
        // Link do waloru
        var a_href = document.createElement('a');
        a_href.setAttribute('href', response[num]['value'][i][0]);
        a_href.innerHTML = response[num]['value'][i][0];
        item_empty_div.appendChild(a_href);
        analyze_item.appendChild(item_empty_div);
        // Cena waloru
        var item_empty_div = document.createElement('div');
        item_empty_div.innerHTML = response[num]['value'][i][3] + "PLN";
        analyze_item.appendChild(item_empty_div);

        // Dzienna zmiana 
        var item_empty_div = document.createElement('div');
        item_empty_div.innerHTML = response[num]['value'][i][4] + " %";
        analyze_item.appendChild(item_empty_div);

        // Procentowa róznica wolumneu od średniej
        var item_empty_div = document.createElement('div');
        item_empty_div.innerHTML = response[num]['value'][i][2] + " %";
        analyze_item.appendChild(item_empty_div);
        analyze_display.appendChild(analyze_item);
    }
    return analyze_display;

}