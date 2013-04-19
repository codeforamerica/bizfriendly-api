var debug = true;

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
  if (debug){
    console.log(whichStep);
  }
});

// Back button
$('.back').click(function (){
  if (debug){
    console.log('Back');
  }
  var backStep = whichStep - 1;
  $('html, body').animate({ scrollTop: $('#link'+backStep).offset().top - body_padding }, 1000);
});

// Next button
$('.next').click(function() {
  if (debug){
    console.log('Next');
  }
  var nextStep = whichStep + 1;
  $('html, body').animate({ scrollTop: $('#link'+nextStep).offset().top - body_padding }, 1000);
});

// Facebook
// FB login
var loggedIn = false;
var fbLogin = function(){
  FB.login(function(response) {
    if (response.authResponse) {
      console.log('User is logged in');
      loggedIn = true;
    } else {
      console.log('User cancelled login or did not fully authorize.');
    }
   }, {scope: 'manage_pages'});
}

var numOfExistingPages = [];
var fbLoginStatus = function(){
  FB.getLoginStatus(function(response) {
    if (debug){
      console.log(response);
    }
    if (response.status === 'connected') {
      // the user is logged in and has authenticated your
      // app, and response.authResponse supplies
      // the user's ID, a valid access token, a signed
      // request, and the time the access token 
      // and signed request each expire
      // var uid = response.authResponse.userID;
      // var accessToken = response.authResponse.accessToken;
      FB.api('/me/accounts/', function(response) {
        numOfExistingPages = response.data.length;
      });
      loggedIn = true;
    } else if (response.status === 'not_authorized') {
      // the user is logged in to Facebook, 
      // but has not authenticated your app
      fbLogin();
    } else {
      // the user isn't logged in to Facebook.
      if (debug){
        console.log('Not logged in.');
      }
      fbLogin();
    }
  });
}

// init the FB JS SDK
window.fbAsyncInit = function() {
  FB.init({
    appId      : '158953284268352', // App ID from the app dashboard
    // channelUrl : 'channel.html', // Channel file for x-domain comms
    status     : true,              // Check Facebook Login status
    cookie     : true, // enable cookies to allow the server to access the session
    // xfbml      : true  // parse XFBML
  });
  if (debug){
    console.log('Facebook has loaded.');
  }
  fbLoginStatus();
}
// Load the SDK asynchronously
(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = "//connect.facebook.net/en_US/all.js";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));


// Steps Functions ---------------------

// If logged in, scroll to step 2
var checkStep1 = function(){
  if (debug){
      console.log('Step 1 running');
    }
  if (whichStep >= 1 && loggedIn){
    clearInterval(t1);
    if (debug){
      console.log('Step 1 stopped');
    }
    var link1Html = $('#link1').html();
    link1Html = link1Html + '<br/> <h2>Alright, you\'re logged in!</h2>'
    $('#link1').html(link1Html);
    if (whichStep == 1){
      $('html, body').delay(2000).animate({ scrollTop: $('#link2').offset().top - body_padding }, 1000); 
    }
  }
}
var t1 = setInterval(checkStep1,1000);

// When we get to step 2, open up the challenge window
var width = window.screen.width;
var height = window.screen.height;
var challengeSiteFeatures = {
  height: height,
  width: width*0.695,
  name: 'challenge',
  center: false
}
var challengeWindow = false;
var checkStep2 = function(){
  if (whichStep >= 2 && loggedIn){
    clearInterval(t2);
    if (debug){
      console.log('Step 2 finished.');
    }
    setTimeout(function(){
      challengeWindow = $.popupWindow('https://www.facebook.com/pages/create/', challengeSiteFeatures);
    }, 2000);
    setTimeout(function(){
      var link2Html = $('#link2').html();
      link2Html = link2Html + '<br/> <h2>You\'re welcome.</h2>'
      $('#link2').html(link2Html);
    }, 5000);
    if (whichStep == 2){
      $('html, body').delay(7000).animate({ scrollTop: $('#link3').offset().top - body_padding }, 1000); 
    }
  }
}
var t2 = setInterval(checkStep2,1000);

// Check for new page
var newPage = {};
var checkStep3 = function(){
  if (whichStep >= 3 && loggedIn){
    
    FB.api('/me/accounts/', function(response) {
      if (debug){
        console.log('My account:');
        console.log(response);
        var link3Html = $('#link3').html();
        newPage = response.data[0];
        link3Html = link3Html + "Debug mode: Using "+response.data[0].name;
        $('#link3').html(link3Html);
        clearInterval(t3);
        if (whichStep == 3){
          $('html, body').delay(5000).animate({ scrollTop: $('#link4').offset().top - body_padding }, 1000);
        }
      }
      if (numOfExistingPages < response.data.length){
        clearInterval(t3);
        if (debug){
          console.log('Step 3 finished.');
          console.log(response.data[response.data.length-1]);
        }
        newPage = response.data[response.data.length-1];
        var link3Html = $('#link3').html();
        link3Html = link3Html + '<br/> <p>Awesome! You created a Facebook page called <h2>'+newPage.name+'</h2></p>'
        $('#link3').html(link3Html);

        if (whichStep == 3){
          $('html, body').delay(5000).animate({ scrollTop: $('#link4').offset().top - body_padding }, 1000);
        }
      }
    });
  }
}
var t3 = setInterval(checkStep3,1000);

// Once they add a description or a website, go to next step.
var checkStep4 = function(){
  if (whichStep >= 4 && loggedIn){
    
    FB.api(newPage.id, function(response) {
      if (debug){
        console.log('Page:');
        console.log(response);
        clearInterval(t4);
      }
    
      if(response.hasOwnProperty('about')){
        if(debug){
          console.log(response.about);
        }
        var link4Html = $('#link4').html();
        link4Html = link4Html + '<br/>You gave' + newPage.name;
        link4Html = link4Html + 'a description of' + response.about;
        $('#link4').html(link4Html);
      }
      if(response.hasOwnProperty('website')){
        if(debug){
          console.log(response.website);
        }
        var link4Html = $('#link4').html();
        link4Html = link4Html + 'and set the website to: ' + response.website;
        $('#link4').html(link4Html);
      }
    });
    //   if (numOfExistingPages < response.data.length){
    //     clearInterval(t4);
    //     if (debug){
    //       console.log('Step 4 finished.');
    //       console.log(response.data[response.data.length-1]);
    //     }
    //     newPage = response.data[response.data.length-1];
    //     var link4Html = $('#link4').html();
    //     link4Html = link4Html + '<br/> <p>Awesome! You created a Facebook page called <h2>'+newPage.name+'</h2></p>'
    //     $('#link4').html(link4Html);

    if (whichStep == 4){
      $('html, body').delay(5000).animate({ scrollTop: $('#link5').offset().top - body_padding }, 1000);
    }
    //   }
    // });
  }
}
var t4 = setInterval(checkStep4,1000);


// Check step 6 for fb login
// var step6login = function(){
//   if(whichStep >= 6){
//     clearInterval(t6);
//     // Need to be logged in after step 6
//     fbLoginStatus();
//     clearInterval(t6login); // Kill the loop
//   }
// }

// var checkStep6 = function(){
//   if (whichStep >= 6){
//     fbLoginStatus();
//     // console.log('step6');
//     if (loggedIn){
//       // console.log(loggedIn);
//       clearInterval(t6); // Kill the loop
//       if (whichStep == 6){
//         var link6Html = $('#link6').html();
//         link6Html = link6Html + '<br/> <h2>Well Done!</h2>'
//         $('#link6').html(link6Html);
        
//         $('html, body').delay(1000).animate({ scrollTop: $('#link7').offset().top - body_padding }, 1000);
//       }
//     }   
//   }
// }

// // var t6login = setInterval(step6login,1000);
// var t6 = setInterval(checkStep6,1000);


// var checkStep7 = function(){
//   if (whichStep >= 7){
//     // Check if they have created any pages
//     FB.api('/me/accounts/', function(response) {
//       // console.log('Response:')
//       // console.log(response);

//       var page_id = response.data[fb_page].id;
//       // console.log('Page id: ');
//       // console.log(page_id);
//       // console.log
//       FB.api(page_id.toString(), function(response) {
//         // console.log('fbo_page_response')
//         // console.log(response);
//         if (response.hasOwnProperty('about')){
//           clearInterval(t7);
//           var link7Html = $('#link7').html();
//           link7Html = link7Html + '<br/> <h2>Well Done!</h2>'
//           $('#link7').html(link7Html);
          
//           $('html, body').delay(1000).animate({ scrollTop: $('#link8').offset().top - body_padding }, 1000);
//         }
//       });

      
//     });
//     // Check if description of page is filled in
//   }
// }

// // var t6login = setInterval(step6login,1000);
// var t7 = setInterval(checkStep7, 1007);


// var checkStep8 = function(){
//   if (whichStep >= 8){
//     // Check if they have created any pages
//     FB.api('/me/accounts/', function(response) {
//       var page_id = response.data[fb_page].id;
//       FB.api(page_id.toString()+'/picture', function(response) {
//         console.log(response.data.is_silhouette);
//         if(!response.data.is_silhouette){
//           clearInterval(t8);
//           var link8Html = $('#link8').html();
//           link8Html = link8Html + '<br/> <h2>Well Done!</h2>'
//           $('#link8').html(link8Html);
          
//           $('html, body').delay(1000).animate({ scrollTop: $('#link9').offset().top - body_padding }, 1000);
//         }
//       });

      
//     });
//     // Check if description of page is filled in
//   }
// }

// // var t6login = setInterval(step6login,1000);
// var t8 = setInterval(checkStep8, 1007);


// var checkStep7 = function(){
//   // Login the How to City app
//   function login() {
//     FB.login(function(response) {
//         if (response.authResponse) {
//             // connected
//         } else {
//             // cancelled
//         }
//     });
//   }

  
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

// console.log('Welcome!  Fetching your information.... ');
      // FB.api('/me', function(response) {
      //  console.log('Good to see you, ' + response.name + '.');
      // });
      // FB.api('/me/accounts/', function(response) {
      //   console.log(response);
      // });

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
