document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#remove-wishlist').addEventListener('click', () => remove_wishlist(event));

});


function remove_wishlist(event) {

    fetch(`/wish/${event.target.name}`, {
      method: 'POST',
      body: JSON.stringify({
      })
    })

    window.location.reload();
    return false;
}