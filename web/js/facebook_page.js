// Scroll bar and which step
var whichStep = 1;
var scroll_height;
var doc_height = $('body').height();
var scroll_pct;
var numOfSections = $('section').length;
var sectionPercentHeight = 100 / numOfSections;
var body_padding = parseInt($('body').css('padding-top'), 10);

$(window).scroll(function() {
  scroll_height = $(window).scrollTop();
  scroll_pct = (scroll_height / doc_height * 100) + 5.5; // Give it a little buffer
  $('.progress .bar').css('width',scroll_pct+'%');
  whichStep = Math.ceil(scroll_pct / sectionPercentHeight);
});

// Back button
$('.back').click(function (){
  var backStep = whichStep - 1;
  $('html, body').animate({ scrollTop: $('#link'+backStep).offset().top - body_padding }, 1000);
});

// Next button
$('.next').click(function() {
  var nextStep = whichStep + 1;
  $('html, body').animate({ scrollTop: $('#link'+nextStep).offset().top - body_padding }, 1000);
});


// Facebook
// init the FB JS SDK
FB.init({
  appId      : '158953284268352', // App ID from the app dashboard
  channelUrl : 'channel.html', // Channel file for x-domain comms
  status     : true,              // Check Facebook Login status
  cookie     : true, // enable cookies to allow the server to access the session
  xfbml      : true  // parse XFBML
});

// Load the SDK asynchronously
// (function(d, s, id){
//    var js, fjs = d.getElementsByTagName(s)[0];
//    if (d.getElementById(id)) {return;}
//    js = d.createElement(s); js.id = id;
//    js.src = "http://connect.facebook.net/en_US/all.js";
//    fjs.parentNode.insertBefore(js, fjs);
//  }(document, 'script', 'facebook-jssdk'));

// FB login
var fbLogin = function(){
  FB.login(function(response) {
    if (response.authResponse) {
      // console.log('Welcome!  Fetching your information.... ');
      // FB.api('/me', function(response) {
      //  console.log('Good to see you, ' + response.name + '.');
      // });
      // FB.api('/me/accounts/', function(response) {
      //   console.log(response);
      // });
      console.log('User is logged in');
    } else {
      console.log('User cancelled login or did not fully authorize.');
    }
   }, {scope: 'manage_pages'});
}

var loggedIn = false;
var fbLoginStatus = function(){
  FB.getLoginStatus(function(response) {
    console.log(response);
    if (response.status === 'connected') {
      // the user is logged in and has authenticated your
      // app, and response.authResponse supplies
      // the user's ID, a valid access token, a signed
      // request, and the time the access token 
      // and signed request each expire
      // var uid = response.authResponse.userID;
      // var accessToken = response.authResponse.accessToken;
      // FB.api('/me/accounts/', function(response) {
      //     console.log(response);
      //   });
      loggedIn = true;
    } else if (response.status === 'not_authorized') {
      // the user is logged in to Facebook, 
      // but has not authenticated your app
      fbLogin();
    } else {
      // the user isn't logged in to Facebook.
      fbLogin();
    }
  });
}


// Check step 6 for fb login
var step6login = function(){
  if(whichStep >= 6){
    // clearInterval(t6);
    // Need to be logged in after step 6
    fbLoginStatus();
    clearInterval(t6login); // Kill the loop
  }
}

var checkStep6 = function(){
  if (loggedIn && whichStep >=6){
    var link6Html = $('#link6').html();
    link6Html = link6Html + '<br/> <h2>Well Done!</h2>'
    $('#link6').html(link6Html);

    clearInterval(t6); // Kill the loop
  }
  if (loggedIn && whichStep == 6){
    $('html, body').delay(1000).animate({ scrollTop: $('#link7').offset().top - body_padding }, 1000);
  }
}

var t6login = setInterval(step6login,1000);
var t6 = setInterval(checkStep6,1001);

// var checkStep7 = function(){
//   // Login the How to City app
//   // function login() {
//   //   FB.login(function(response) {
//   //       if (response.authResponse) {
//   //           // connected
//   //       } else {
//   //           // cancelled
//   //       }
//   //   });
//   // }

  
//   if (whichStep == 7){
//    //  FB.login(function(response) {
//    // if (response.authResponse) {
//      // console.log('Welcome!  Fetching your information.... ');
//      FB.api('/me/accounts', function(response) {
//        console.log(response);
//      });
//    // } else {
//    //   console.log('User cancelled login or did not fully authorize.');
//    // }
//  // });
//     // login();
//     clearInterval(t7);
//   } 

// }


// var t7 = setInterval(checkStep7,1000);





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
