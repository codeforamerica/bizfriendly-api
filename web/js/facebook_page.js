// Facebook
FB.init({
  appId      : '158953284268352', // App ID from the app dashboard
  status     : true               // Check Facebook Login status
});

// Scroll bar and which step
var whichStep = 1;
var scroll_height;
var doc_height = $(document).height();
var scroll_pct;
var numOfSections = $('section').length - 1;
console.log(numOfSections);
var sectionPercentHeight = 100 / numOfSections
if(whichStep < 8){ // HACK HACK HACK
  sectionPercentHeight = sectionPercentHeight - 1;
}
console.log(sectionPercentHeight);

$(window).scroll(function() {
  scroll_height = $(window).scrollTop();
  scroll_pct = (scroll_height / doc_height * 100);
  $('.progress .bar').css('width',scroll_pct+'%');
  whichStep = Math.ceil(scroll_pct / sectionPercentHeight);
});

// Next button
$('.next').click(function() {
  // if (whichStep < 6){ // Hack hack hack
  //   whichStep = whichStep + 1;
  // }
  var nextStep = whichStep + 1;
  console.log('#link'+nextStep);
    $('html, body').animate({ scrollTop: $('#link'+nextStep).offset().top }, 1000);
});



// Check step 6 for fb login
var fbLoginStatus = false;
var checkStep6 = function(){
  console.log(whichStep);
  if(whichStep == 6){
    FB.getLoginStatus(function(response) {
      console.log(response);
      if (response.status === 'connected') {
        fbLoginStatus = true;
        // the user is logged in and has authenticated your
        // app, and response.authResponse supplies
        // the user's ID, a valid access token, a signed
        // request, and the time the access token 
        // and signed request each expire
        var uid = response.authResponse.userID;
        var accessToken = response.authResponse.accessToken;
      } else if (response.status === 'not_authorized') {
        // the user is logged in to Facebook, 
        // but has not authenticated your app
      } else {
        // the user isn't logged in to Facebook.
      }
    },true);
    if (fbLoginStatus){
      $('html, body').animate({ scrollTop: $('#link7').offset().top }, 1000);
    }
    if (whichStep > 6){
      clearInterval(t);
    }
  }
}

var t = setInterval(checkStep6,1000);





// JUNK ---------

// // Runs once Facebook has loaded
// window.fbAsyncInit = function() {
//   // init the FB JS SDK
//   FB.init({
//     appId      : '158953284268352', // App ID from the app dashboard
//     status     : true               // Check Facebook Login status
//   });

//   // Check for step 6 and facebook login
//   FB.Event.subscribe('auth.authResponseChange', function(response) {
//     alert('The status of the session is: ' + response.status);
//   });

// };

// // Check fb login status
// var fbLoginStatus = false;
 
//   var checkFBLogin = function(){
//     FB.getLoginStatus(function(response) {
//     console.log(fbLoginStatus);
//     if (response.status === 'connected') {
//       fbLoginStatus = true;
//     // the user is logged in and has authenticated your
//     // app, and response.authResponse supplies
//     // the user's ID, a valid access token, a signed
//     // request, and the time the access token 
//     // and signed request each expire
//     var uid = response.authResponse.userID;
//     var accessToken = response.authResponse.accessToken;
//   } else if (response.status === 'not_authorized') {
//     // the user is logged in to Facebook, 
//     // but has not authenticated your app
//   } else {
//     // the user isn't logged in to Facebook.
//   }
//  },true);
//   };


// // Load the SDK asynchronously
// (function(d, s, id){
//    var js, fjs = d.getElementsByTagName(s)[0];
//    if (d.getElementById(id)) {return;}
//    js = d.createElement(s); js.id = id;
//    js.src = "http://connect.facebook.net/en_US/all.js";
//    fjs.parentNode.insertBefore(js, fjs);
//  }(document, 'script', 'facebook-jssdk'));




  // // Update current sections

  // // Step 6 - Facebook login
  // var whichStep = Math.ceil(scroll_pct / 5.5);
  // console.log(whichStep);
  // if(!step6 && whichStep == 6){ // Fires once
  //   step6 = true;
  //   console.log('step6: '+ step6);
    

  //   checkFBLogin();
  //   console.log('loginStatus: '+ loginStatus);
  //   if (loginStatus){
  //     // $('html, body').animate({ scrollTop: sections.offset().top }, 1000);
  //     console.log('In loop:' + sections);
  //   }
  // }
