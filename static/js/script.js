document.getElementById("search_input").addEventListener('keyup', () => {
    var req = new XMLHttpRequest();
    const data = new FormData()
    req.open('POST', '/', true);
    data.append('search_value', document.getElementById('search_input').value)
    req.onload =()=>{
        if (req.status !== 200){
            console.log(req);
            console.log('Błąd połaczenia');
        }
    };
    req.send(data);
})