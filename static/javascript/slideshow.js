var slideIndex = 1;
var pageIndex = 0;
window.onload = function() {
  allItems(1);
  showCards(0);
}

function plusSlides(n, card_ind) {
  showSlides(slideIndex += n, card_ind);
}
function plusPages(n){
    showCards(pageIndex += n);
}
function showCards(n){
    var cards = document.querySelectorAll(".card");
    console.log(parseInt(cards.length/ 10))
    console.log(cards.length)
    if (n > parseInt(cards.length / 10) ) {
        pageIndex = 0;
        n = 0;
     }
     console.log(n)
    for (i=0; i < cards.length; i++){
       if (i >= (0 + (n*10)) && i <= (9 + (n*10))){
            cards[i].style.display = "block";
       } else{
            cards[i].style.display = "none";
       }
    }
}

function showSlides(n, card_ind) {
  var i;
  var slides = document.querySelectorAll(".slideshow-container--" + card_ind.toString() + " .mySlides");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }

  slides[slideIndex-1].style.display = "block";

}
function allItems(n) {
  var items = document.getElementsByClassName('card')
  for (i = 0; i < items.length; i++) {
      showSlides(n, i);

  }

}