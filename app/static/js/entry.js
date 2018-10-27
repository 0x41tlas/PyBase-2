var partName = document.getElementById('name');
var locate = document.getElementById('locate');
var description = document.getElementById('description');
var manufacturer = document.getElementById('manufacturer');
var quant = document.getElementById('quant');
var enter = document.getElementById('enter');

enter.addEventListener('click', function() {
    fetch('/entry', {
        method: 'POST',
        body: JSON.stringify({
            partName: partName.value,
            locate: locate.value,
            quant: quant.value,
            description: description.value,
            manufacturer: manufacturer.value
        }),
        headers:{'Content-Type': 'application/json'}
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        alert(data)
    });
});
