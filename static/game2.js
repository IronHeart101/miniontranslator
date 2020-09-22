var links=["static/images/dice1.png","static/images/dice2.png","static/images/dice3.png","static/images/dice4.png","static/images/dice5.png","static/images/dice6.png"];
function dice(links){

var generate=links.length;
var randomNumber=Math.floor(Math.random()*generate);
var roll=links[randomNumber];
document.querySelector("img").setAttribute("src",roll);



 var randomNumber1=Math.floor(Math.random()*generate);
 var roll1=links[randomNumber1];
 document.querySelector("img.img2").setAttribute("src",roll1);

 if(randomNumber==randomNumber1){
   document.querySelector("h1").innerHTML="Draw!";
 }
 else if(randomNumber>randomNumber1){
     document.querySelector("h1").innerHTML="🚩Player 1 wins!";
 }
 else
   document.querySelector("h1").innerHTML="Player 2 wins!🚩";
  }
