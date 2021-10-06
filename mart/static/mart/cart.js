function update_cart(id) {

    fetch('/update-cart', {
      method: 'PUT',
      body: JSON.stringify({
        product: id,
        action: "remove",
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

    window.location.reload();
    return false;
}

function update_value(id) {

    value = document.getElementById(`new-value-${id}`).value;

    fetch('/update-cart', {
      method: 'PUT',
      body: JSON.stringify({
        product: id,
        value: value,
        action: "update",
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

    window.location.reload();
    return false;
}