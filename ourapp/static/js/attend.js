take_photo_btn.addEventListener("click", function(e){

    e.preventDefault();
  
    var snap = takeSnapshot();
  
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
  
      // Save the picture in base64
      pic = hidden_canvas.toDataURL('image/png')
  
      // Get ready to send to the server
      var xhr = new XMLHttpRequest();
      // if the server returns a match, load the welcome page
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          if (xhr.response == "error" || xhr.response=="nomatch") {
            document.getElementById("error").innerHTML = "Sorry, we didn't recognize you!"
            setTimeout(function() {
              document.getElementById("error").innerHTML=""
            }, 2000);
          }
          else{
            document.getElementById("success").innerHTML = "Welcome " + xhr.response
            setTimeout(function() {
              document.getElementById("success").innerHTML=""
            }, 2000);
          }
        }
      }
  
      // Send the pic to the the server
      xhr.open('POST', '/takeattend/A', true);
      xhr.send(pic)
  
      return pic
    }
  }
  