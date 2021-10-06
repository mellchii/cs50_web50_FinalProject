document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#add-cart').addEventListener('click', () => add_cart(event));
    document.querySelector('#add-wishlist').addEventListener('click', () => add_wishlist(event));
    document.querySelector('#remove-wishlist').addEventListener('click', () => add_wishlist(event));

    star_handle();
});

function submit_review(id) {

    const body = document.querySelector('#review-body').value;
    fetch(`/review/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          body: body
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

function star_handle() {
    // get all stars
    const one = document.getElementById('star1')
    const two = document.getElementById('star2')
    const three = document.getElementById('star3')
    const four = document.getElementById('star4')
    const five = document.getElementById('star5')

    const star_select = (select) => {
        switch(select){
            case 'star1': {
                two.classList.remove('checked')
                three.classList.remove('checked')
                four.classList.remove('checked')
                five.classList.remove('checked')
                return
            }
            case 'star2': {
                two.classList.add('checked')
                three.classList.remove('checked')
                four.classList.remove('checked')
                five.classList.remove('checked')
                return
            }
            case 'star3': {
                two.classList.add('checked')
                three.classList.add('checked')
                four.classList.remove('checked')
                five.classList.remove('checked')
                return
            }
            case 'star4': {
                two.classList.add('checked')
                three.classList.add('checked')
                four.classList.add('checked')
                five.classList.remove('checked')
                return
            }
            case 'star5': {
                two.classList.add('checked')
                three.classList.add('checked')
                four.classList.add('checked')
                five.classList.add('checked')
                return
            }
        }
    }

    const star_array = [one, two, three, four, five]

    star_array.forEach(item => item.addEventListener('mouseover', (event)=>{
        star_select(event.target.id);
    }))

    star_array.forEach(item => item.addEventListener('click', (event)=>{
        let rate = star_array.indexOf(item) + 1;
        let id = event.target.title;
        console.log(rate);
        console.log(id);
        document.getElementById('rate-text').innerHTML = `You rated this product ${rate} star!`;

        fetch(`/review/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              rating: rate
          })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);

        });
    }))
}

function add_cart(event) {
    console.log('Add Cart Button Clicked');

    quantity = document.getElementById('quantity').value

    if (quantity == '' || quantity < 1){
        console.log('Empty Qty')
        document.getElementById('message').innerHTML = `<li><em style="color:red">Enter Quantity greater than 0</em></li>`;
        document.getElementById('quantity').value = '';
        return false
    }

    fetch('/update-cart', {
      method: 'POST',
      body: JSON.stringify({
          product: event.target.name,
          quantity: quantity,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        document.getElementById('message').innerHTML = `<li><em>Product added to cart</em></li>`;
        document.getElementById('quantity').value = '';
        return cart_count()
    });
}

function cart_count(){
    fetch('/cart-count')
    .then(response => response.json())
    .then(order => {

        console.log(order);
        document.getElementById('cart-count').innerHTML = order.item_total;

  });
}

function add_wishlist(event) {

    event.target.style.display = 'none';
    if (event.target.id === 'remove-wishlist'){
        document.querySelector('#add-wishlist').style.display = 'block';
    }
    else {
        document.querySelector('#remove-wishlist').style.display = 'block';
    }

    fetch(`/wish/${event.target.name}`, {
      method: 'POST',
      body: JSON.stringify({
      })
    })
}
