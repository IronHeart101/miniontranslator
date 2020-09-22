var buttonColors = ["red", "blue", "green", "yellow"];

var gamePattern = [];

var userClickedPattern=[];

var started=false;
var level=0;

$(document).keypress(function()
{
if(!started){
  $("#level-title").text("Level " + level);
   nextSequence();
   started = true;

}

});
$(".btn").click(function(){
  var userChosenColor=$(this).attr("id");
  userClickedPattern.push(userChosenColor);
//  console.log(userClickedPattern);
  playSound(userChosenColor);
  animatePress(userChosenColor);
  checkAnswer(userClickedPattern.length-1);

});


function checkAnswer(currentLevel){
if(userClickedPattern[currentLevel]===gamePattern[currentLevel]){
  console.log("success");

  if (userClickedPattern.length === gamePattern.length){

     //5. Call nextSequence() after a 1000 millisecond delay.
     setTimeout(function () {
       nextSequence();
     }, 1000);

   }

}else{
  console.log("wrong");
  playSound("wrong");

  $("body").addClass("game-over");
  setTimeout(function(){
    $("body").removeClass("game-over");
  },200);
  $("#level-title").text("Game over!Press any key to restart")
  startOver();
}
}

function nextSequence() {

  userClickedPattern=[];
  level++;

  $("#level-title").text("Level "+level);

  var randomNumber = Math.floor(Math.random() * 4);
  var randomChosenColor = buttonColors[randomNumber];
  gamePattern.push(randomChosenColor);


  //1. Use jQuery to select the button with the same id as the randomChosenColour
  //2. Use Google/Stackoverflow to figure out how you can use jQuery to animate a flash to the button selected in step 1.
  $("#" + randomChosenColor).fadeIn(100).fadeOut(100).fadeIn(100);

  //3. Use Google/Stackoverflow to figure out how you can use Javascript to play the sound for the button colour selected in step 1.
playSound(randomChosenColor);
//animatePress(randomChosenColour);

}

function playSound(name){


  //3. Take the code we used to play sound in the nextSequence() function and add it to playSound().
  var audio = new Audio("./sounds"+ name + ".mp3");
  audio.play();

}


function animatePress(currentColor){
  $("#"+currentColor).addClass("pressed");

  setTimeout(function(){
    $("#"+currentColor).removeClass("pressed");
  },100);
}





function startOver(){
    level=0;
  gamePattern=[];
  started=false;

}
