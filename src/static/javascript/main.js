let updateBtn = document.getElementsByClassName("update-button")

for(let i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log(productId, action)
        if (user == 'AnonymousUser'){
            console.log('Not Authenticared User')
        }else{
            Posttoken(productId, action)
        }
    })

}function Posttoken(productId, action) {
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
        location.reload()
    })
}