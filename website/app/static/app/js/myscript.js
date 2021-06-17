$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function () {
    var id=$(this).attr("pid").toString();
    console.log(id)
    var eml=this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id: id
        },
        success:function(data){
            
           eml.innerText=data.quantity
           document.getElementById("amount").innerText=data.amount
           document.getElementById("totalamount").innerText=data.totalamount


        }
    })
})



$('.minus-cart').click(function () {
    var id=$(this).attr("pid").toString();
    console.log(id)
    var eml=this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id: id
        },
        success:function(data){
            
           eml.innerText=data.quantity
           document.getElementById("amount").innerText=data.amount
           document.getElementById("totalamount").innerText=data.totalamount


        }
    })
})

$('.remove-cart').click(function () {
    var a = 2; 
    console.log(a);
    console.log("abcd")
    var id=$(this).attr("pid").toString();
    console.log(id)
    var eml=this
    console.log(id)
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id: id
        },
        success:function(data){
            
           document.getElementById("amount").innerText=data.amount
           document.getElementById("totalamount").innerText=data.totalamount
           eml.parentNode.parentNode.parentNode.parentNode.remove()


        }
    })
})


console.log('9999999999999')
var updateBtns = document.getElementsByClassName('update-cart')
console.log(updateBtns)
console.log('977777')
console.log(updateBtns.length)
for (i = 0; i < updateBtns.length; i++) {
    console.log('9988888887')
	updateBtns[i].addEventListener('click', function(){
        console.log('1110000111')
        var productId = this.dataset.product
        console.log('1111000033333')
        var action = this.dataset.action
        console.log('happy ending')

        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}
	})
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART1231:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()

}
