document.addEventListener('DOMContentLoaded', function() {

    see_all();

    document.querySelector('#all-view').style.display = 'none';
    document.querySelector('#see').style.display = 'block';
    document.querySelector('#see').addEventListener('click', see_alls);
    document.querySelector('#some').addEventListener('click', see_some);
});

function see_all() {

    document.querySelector('#see').style.display = 'none';
    document.querySelector('#all-view').style.display = 'block';
    document.querySelector('#some').style.display = 'none';

    fetch('/all')
    .then(response => response.json())
    .then(products => {
        products.forEach(product => {
            // Print products
            console.log(product);

            // ... do something else with products ...
            let row_col = document.createElement('div');
            let card = document.createElement('div');
            let anchor = document.createElement('a');
            let image = document.createElement('img');
            let figure = document.createElement('figcaption');
            let title = document.createElement('div');
            let price = document.createElement('div');
            let rate = document.createElement('div');
            let span1 = document.createElement('span');
            let span2 = document.createElement('span');
            let span3 = document.createElement('span');
            let span4 = document.createElement('span');
            let span5 = document.createElement('span');

            row_col.className = "col-md-3";
            card.className = "card card-product-grid";
            anchor.className = "img-wrap";
            figure.className = "info-wrap";
            title.className = "title";
            price.className = "price mt-1";
            rate.style.paddingBottom = "5%";
            span1.className = "fa fa-star";
            span2.className = "fa fa-star";
            span3.className = "fa fa-star";
            span4.className = "fa fa-star";
            span5.className = "fa fa-star";

            if (product.avg_rating == 1){
                span1.classList.add("checked");
            } else if (product.avg_rating == 2){
                span1.classList.add("checked");
                span2.classList.add("checked");
            } else if (product.avg_rating == 3){
                span1.classList.add("checked");
                span2.classList.add("checked");
                span3.classList.add("checked");
            } else if (product.avg_rating == 4){
                span1.classList.add("checked");
                span2.classList.add("checked");
                span3.classList.add("checked");
                span4.classList.add("checked");
            } else if (product.avg_rating == 5){
                span1.classList.add("checked");
                span2.classList.add("checked");
                span3.classList.add("checked");
                span4.classList.add("checked");
                span2.classList.add("checked");
            }

            card.setAttribute("href", `/product/${product.id}`);
            anchor.setAttribute("href", `/product/${product.id}`);
            image.setAttribute("src", `${product.img_url}`);
            image.setAttribute("alt", "No Image");

            title.innerHTML = product.name;
            price.innerHTML = `$${product.price}`;

            rate.appendChild(span1);
            rate.appendChild(span2);
            rate.appendChild(span3);
            rate.appendChild(span4);
            rate.appendChild(span5);
            figure.appendChild(title);
            figure.appendChild(rate);
            figure.appendChild(price);
            anchor.appendChild(image);

            card.appendChild(anchor);
            card.appendChild(figure);

            row_col.appendChild(card);

            document.querySelector('#row-class').appendChild(row_col);

            });
        });
}

function see_some() {

    // Hide all view and show paginate view
    document.querySelector('#paginate-view').style.display = 'block';
    document.querySelector('#all-view').style.display = 'none';
    document.querySelector('#some').style.display = 'none';
    document.querySelector('#see').style.display = 'block';
}

function see_alls() {

    // Hide all view and show paginate view
    document.querySelector('#paginate-view').style.display = 'none';
    document.querySelector('#all-view').style.display = 'block';
    document.querySelector('#some').style.display = 'block';
    document.querySelector('#see').style.display = 'none';

}