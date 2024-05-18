$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            eml.parentNode.parentNode.parentNode.parentNode.remove();
        }
    });
});


function addToCart(productId) {
    window.location.href = '/add-to-cart/?prod_id=' + productId;
}

function addToCart(productId) {
    if (productId) {
        $.ajax({
            url: '/add-to-cart/',
            type: 'GET',
            data: { prod_id: productId },
            success: function(response) {
                // Handle success
            },
            error: function(response) {
                alert('Product ID is missing or invalid.');
            }
        });
    } else {
        alert('Product ID is missing.');
    }
}
