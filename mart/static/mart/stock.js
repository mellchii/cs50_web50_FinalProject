document.addEventListener('DOMContentLoaded', function() {

  // Add event listeners
  document.querySelector('#dashboard').addEventListener('click', dashboard);
  document.querySelector('#sales').addEventListener('click', sales_summary);
  document.querySelector('#supply').addEventListener('click', supply_summary);
  document.querySelector('#inventory').addEventListener('click', edit_inventory);

  document.querySelector('#sales-table').style.display = 'none';
  document.querySelector('#supply-table').style.display = 'none';
  document.querySelector('#inventory-table').style.display = 'none';

  // By default, load dashboard
  dashboard();
});

function dashboard() {
    document.querySelector('#stock-title').innerHTML = "Stock Manager: Dashboard";
    document.querySelector('#sales-table').style.display = 'none';
    document.querySelector('#supply-table').style.display = 'none';
    document.querySelector('#inventory-table').style.display = 'none';
    document.querySelector('#dash-table').style.display = 'inline-flex';
}

function sales_summary() {
    document.querySelector('#stock-title').innerHTML = "Stock Manager: Sales Summary";
    document.querySelector('#sales-table').style.display = 'block';
    document.querySelector('#supply-table').style.display = 'none';
    document.querySelector('#inventory-table').style.display = 'none';
    document.querySelector('#dash-table').style.display = 'none';
}

function supply_summary() {
    document.querySelector('#stock-title').innerHTML = "Stock Manager: Supply Summary";
    document.querySelector('#sales-table').style.display = 'none';
    document.querySelector('#supply-table').style.display = 'block';
    document.querySelector('#inventory-table').style.display = 'none';
    document.querySelector('#dash-table').style.display = 'none';
}

function edit_inventory() {
    document.querySelector('#stock-title').innerHTML = "Stock Manager: Edit Inventory";
    document.querySelector('#sales-table').style.display = 'none';
    document.querySelector('#supply-table').style.display = 'none';
    document.querySelector('#inventory-table').style.display = 'block';
    document.querySelector('#dash-table').style.display = 'none';
}

function update_stock(event, id) {
    value = event.target.previousElementSibling.value

     // Ensure input is greater than 0
    if ((parseInt(value) < 1) || (value == "")){
        alert("Enter a value greater than '0'")
        event.target.previousElementSibling.value = 0;
        return false;
    }

    console.log("Submit Button Clicked")
    console.log(id)
    console.log(value)

    fetch(`/edit/${id}`)
    .then(response => response.json())
    .then(product => {
        // Print current stock balance
        console.log(product.stock);
        new_stock = product.stock + parseInt(value)

        return stock_update(event, id, new_stock)

      });
}

function stock_update(event, id, new_stock){

    fetch(`/edit/${id}`, {
      method: 'POST',
      body: JSON.stringify({
        quantity: parseInt(value)
      })
    })

    fetch(`/edit/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          stock: new_stock
      })
    })
    .then(response => response.json())
    .then(product => {
      // Print updated stock balance
      console.log(product);
      console.log(product.stock);

      // ... update stock in DOM ...
      document.querySelector(`#stock-${id}`).innerHTML = product.stock;

    });
    event.target.previousElementSibling.value = 0;
}