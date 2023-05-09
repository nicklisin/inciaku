function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const deliveryCheck = document.querySelectorAll("input[name='delivery-input']")
const addressBox = document.querySelector('.address-box')

if (deliveryCheck) {
    deliveryCheck.forEach(item => {
    item.addEventListener('click', (e)=>{
        if (e.target.id === 'delivery'){
            addressBox.style = 'display:block;'
        } else {
            addressBox.style = 'display:none;'
        }
        })
    })
}


let buttons = document.querySelectorAll('.update-cart')
if(buttons){
    buttons.forEach((button)=>{
        button.addEventListener('click', upt)
})
}

const quant = document.querySelector('.basket-q a')

function upt(event){
    event.preventDefault()
    let productId = event.target.dataset.product
    let action = event.target.dataset.action

    if(user === 'AnonymousUser'){
        cookieAction(productId, action, event)
        let cart = JSON.parse(getCookie('cart'))
        if (cart){
            let cart_quantity = 0
            for(let key in cart){
                cart_quantity += cart[key].quantity
            }
            quant.innerText = cart_quantity
        }

        const basketTotalGoods = document.querySelector('#basket-goods-total')
        const basketDelivery = document.querySelector('#basket-delivery-total')
        const basketTotal = document.querySelector('#basket-total')
        if(basketTotalGoods){
            const totalUrl = '/get_cart_total/'
            fetch(totalUrl)
                .then(res => res.json())
                .then(data => {
                    basketTotalGoods.innerText = Math.round(data)
                    basketDelivery.innerText = 0
                    basketTotal.innerText = Math.round(data)
                })
        }

    } else {
        sendAction(productId, action)
        cartInputUpdate(cart, productId, action)
    }
    // location.reload()
}

function cookieAction(productId, action, event){
    let cart = JSON.parse(getCookie('cart'))
    cartInputUpdate(cart, productId, action)
    if(action === 'add'){
        if (cart[productId] === undefined){
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
            if(cart[productId]['quantity'] > 1){
                const reduceBtn = document.getElementById(`reduce-q-${productId}`)
                if(reduceBtn){
                    reduceBtn.disabled = false
                }
            }
        }
    }
    if(action === 'reduce-q'){
        if(cart[productId]['quantity'] > 1){
            cart[productId]['quantity'] -= 1
            if(cart[productId]['quantity'] === 1){
                event.target.disabled = true;
            }
        } else {
            delete cart[productId]
            document.getElementById(`basket-good-${productId}`).remove()
        }
    }
    if(action === 'remove'){
        delete cart[productId]
        document.getElementById(`basket-good-${productId}`).remove()
        if(Object.keys(cart).length === 0){
            document.getElementById('full-basket').style = 'display: none;'
            document.getElementById('empty-basket').style = 'display: block;'
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
}

function cartInputUpdate(cart, productId, action){
    const inputToUpdate = document.getElementById(`input-${productId}`)
    if(inputToUpdate){
        let quantityToUpdate = 0
        let cartIsNotEmpty = Object.keys(cart).length
        if (cartIsNotEmpty){
            quantityToUpdate = cart[productId]['quantity']
        }
        if(action === 'add'){
            if (cart[productId] === undefined){
                quantityToUpdate = 1
            } else {
                quantityToUpdate += 1
            }
        }
        if(action === 'reduce-q'){
            if(cart[productId]['quantity'] > 1){
                quantityToUpdate -= 1
            } else {
                quantityToUpdate = 0
            }
        }
        if(action === 'remove'){
            quantityToUpdate = 0
        }
        inputToUpdate.value = quantityToUpdate
    }
}

function sendAction(productId, action){
    const url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        quant.innerText = data['cart_quantity']
        window.location.reload()
    })
}

