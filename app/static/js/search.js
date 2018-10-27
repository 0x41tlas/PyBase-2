var query = document.getElementById('query');
var search = document.getElementById('search');
var resultDiv = document.getElementById('resultDiv');

var resultTable = document.getElementById('resultTable');
var resultRows = document.getElementsByClassName('resultRows');

function deleteElement(id) {
    entry = document.getElementById(id).parentNode
    confirmDelete = confirm("Are you sure you want to delete this entry?")
    if (confirmDelete) {
        sendPOST({deleteEntry: entry.cells[0].innerHTML})
        entry.remove();
    }
}

function deleteListener(id) {
    document.getElementById(id).addEventListener('click', function() {
        deleteElement(id);
    });
}

function clearResults() {
    if (resultRows.length > 0) {
        var resLen = resultRows.length;
        for (var i=0; i<resLen; i++) {
            resultRows[0].remove();
        }
    }
}

function sendPOST(body) {
    fetch('/search', {
        method: 'POST',
        body: JSON.stringify(body),
        headers:{'Content-Type': 'application/json'}
    })
}

function newTable(data, tableName) {
    var rowNum = data[0];
    newRow = tableName.insertRow();

    for (var i=0; i<data.length; i++) {
        newRow.insertCell().innerText = data[i];
    };
    newRow.insertCell().innerText = "X";

    newRow.cells[6].className = "x";
    newRow.cells[6].id = 'cell' + rowNum;
    newRow.className = "resultRows";

    deleteListener(newRow.cells[6].id);
}

search.addEventListener('click', function() {
    clearResults();
    fetch('/search', {
        method: 'POST',
        body: JSON.stringify({search: query.value}),
        headers:{'Content-Type': 'application/json'}
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        for(var i=0; i<data.length; i++) {
            newTable(data[i], resultTable);
        }
    });
});
