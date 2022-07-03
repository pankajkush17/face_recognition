// Modified from https://tutorialzine.com/2016/07/take-a-selfie-with-js

// References to all the element we will need.
var delete_photo_btn = document.querySelector('#delete-photo'),
    login_button = document.querySelector('#login'),
    take_photo_btn = document.querySelector('#take-photo');

take_photo_btn.addEventListener("click", function(e){

  e.preventDefault();

  var snap = takeSnapshot();

  // Show image
  image.setAttribute('src', snap);
  // image.classList.add("visible");

  // Enable delete and save buttons
  delete_photo_btn.classList.remove("disabled");

  take_photo_btn.classList.add("disabled");

  // Set the href attribute of the download button to the snap url.

  // Pause video playback of stream.
  video.pause();
});


delete_photo_btn.addEventListener("click", function(e){
  e.preventDefault();

  // Hide image.
  image.setAttribute('src', "");

  // Disable delete button, enable take photo button
  delete_photo_btn.classList.add("disabled");
  take_photo_btn.classList.remove("disabled");

  // Resume playback of stream.
  video.play();
});


login_button.addEventListener("click", function(e) {
  // Make a new FormData object and put the data form the form in it
  var formData = new FormData(document.forms['form']);

  // Add the base64 image from the canvas to the form
  formData.append('userpic', document.querySelector('canvas').toDataURL('image/png'));

  // Send the form to the server via XML HTTP request
  var xhr = new XMLHttpRequest();
  // If the server returns and error, print it. Otherwise, redirect the indicated route
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.response == "error") {
        document.getElementById("error").innerHTML = "Make sure you enter your full name and take a proper picture of your face!";
        setTimeout(function() {
          document.getElementById("error").innerHTML=""
        }, 2000);
      }
      else if(xhr.response == "user"){
        document.getElementById("error").innerHTML = "Sorry that username is not valid.";
        setTimeout(function() {
          document.getElementById("error").innerHTML=""
        }, 2000);
      }
      else if(xhr.response == "nomatch"){
        document.getElementById("error").innerHTML = "Sorry we didnt find you.Please register or try again :).";
        setTimeout(function() {
          document.getElementById("error").innerHTML=""
        }, 2000);
      }
      else if(xhr.response = "match") {
        location.replace('/');
      }
    }
  }

  xhr.open('POST', '/login', true);
  xhr.send(formData)
});


function takeSnapshot(){
  // Here we're using a trick that involves a hidden canvas element.

  var hidden_canvas = document.querySelector('canvas'),
      context = hidden_canvas.getContext('2d');

  var width = video.videoWidth,
      height = video.videoHeight;

  if (width && height) {

    // Setup a canvas with the same dimensions as the video.
    hidden_canvas.width = width;
    hidden_canvas.height = height;

    // Make a copy of the current frame in the video on the canvas.
    context.drawImage(video, 0, 0, width, height);

    pic = hidden_canvas.toDataURL('image/png')

    // Turn the canvas image into a dataURL that can be used as a src for our photo.
    return hidden_canvas.toDataURL('image/png');
    // return pic
  }
}
