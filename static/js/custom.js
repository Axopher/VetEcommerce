$(document).ready(function() {
    // add to cart
    $('.add_to_cart').on('click', function(e) {
        e.preventDefault();
        
        product_id = $(this).attr("data-id");
        action = $(this).attr("data-action");
        url = $(this).attr('data-url');
        data = {
            'product_id':product_id,
            'action':action,
        }
        $.ajax({
            type:"GET",
            url:url,
            data:data,
            success:function(response){
                if(response.status == "Failed"){
                    console.log(response)
                    console.log("raise the error")
                }else{$('#cart_counter').html(response['cartItems']);
                // $('#qty-'+product_id).html(response.cart_counter['cart_count']);
                }
            }
        })
    })

    // delete from cart
    $('.delete_from_cart').on('click', function(e) {
        e.preventDefault();
        
        cartItemID = $(this).attr("data-id");
        action = $(this).attr("data-action");
        url = $(this).attr('data-url');
        data = {
            'cartItemID':cartItemID,
            'action':action,
        }
        $.ajax({
            type:"GET",
            url:url,
            data:data,
            success:function(response){
                console.log(response)
                if(response.status == "Failed"){
                    console.log("raise the error")
                }else{$('#delete_item'+cartItemID).html("");
                // $('#qty-'+product_id).html(response.cart_counter['cart_count']);
                }
            }
        })
    })
});    