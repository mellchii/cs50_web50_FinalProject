function add_wishlist(id) {

    fetch(`/wish/${id}`, {
      method: 'POST',
      body: JSON.stringify({
      })
    })
    window.location.reload();
    return false;
}
