var updateBtn = document.getElementsByClassName("update-button")

for(var i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId, action)
    })
}