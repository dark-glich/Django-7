let updateBtn = document.getElementsByClassName("update-button");
let cart_msg = document.getElementsByClassName("cart-msg");

for(let i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log(productId, action)
        if (user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            Posttoken(productId, action)
        }
        cart_msg[i].style.display = 'block'
        setTimeout(function(){
            cart_msg[i].style.display = 'none'
            location.reload()
        }, 5000)
       
    })

}

function addCookieItem(productId, action){
    console.log('Unauthenticated User');
    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'q':1}
        }else{
            cart[productId]['q'] += 1
        }
    }

    if (action == 'remove'){
        cart[productId]['q'] -= 1

        if(cart[productId]['q'] <= 0){
            delete cart[productId]['q']
        }
    }
    document.cookie = `FruitStore=${JSON.stringify(cart)} ;domain=;path=/`
}

function Posttoken(productId, action) {
    console.log(`Authenticared User : ${user}`)
    let url = '/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log(data)
    })
}