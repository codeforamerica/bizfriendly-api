var debug = false;
var fb_request_time = 10000;
// UI ----------------------------------------------------------------------------------------
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


// Facebook ----------------------------------------------------------------------------------------
// init the FB JS SDK
$(document).ready(function(){

  FB.init({
    appId      : '158953284268352', // App ID from the app dashboard
    //channelUrl : 'http://ondrae.github.io/howtocity/channel.html', // Channel file for x-domain comms
    status     : true,              // Check Facebook Login status
    cookie     : true, // enable cookies to allow the server to access the session
    xfbml      : true  // parse XFBML
  });


  if (debug){
    console.log('Facebook has loaded.');
  }
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

  // Back button
  $('.fbLoginBtn').click(function (){
    if (debug){
      console.log('fbLoginBtn clicked');
    }
    fbLogin();
  });

  var numOfExistingPages = 0;
  // var getExistingPageCount = function(){
  //   FB.api('/me/accounts', function(response){
  //     numOfExistingPages = response.data.length;
  //   });
  // }

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

        loggedIn = true;
      } else if (response.status === 'not_authorized') {
        // the user is logged in to Facebook, 
        // but has not authenticated your app
        loggedIn = false;
      } else {
        // the user isn't logged in to Facebook.
        loggedIn = false;
        if (debug){
          console.log('Not logged in.');
        }
      }
    });
  }
  fbLoginStatus();
  if(debug){
    console.log("Logged in: ", loggedIn);
  }

  // Steps Functions ---------------------

  //Trying to refactor the step functions
  // var checkSteps = function(){
  //   if (debug){
  //     console.log(whichStep);
  //   }
  // }

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
      link1Html = link1Html + '<br/> <h2>Wonderful!</h2>' 
      link1Html = link1Html + 'You\'ve logged in to Facebook and given our app the permissions it needs to teach you how to create Facebook pages.'
      $('#link1').html(link1Html);

      // Important for step 4
      FB.api('/me/accounts/', function(response) {
        numOfExistingPages = response.data.length;
      });


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
      }, 3000);
      if (whichStep == 2){
        $('html, body').delay(6000).animate({ scrollTop: $('#link3').offset().top - body_padding }, 1000); 
      }
    }
  }
  var t2 = setInterval(checkStep2,1000);

  // Check for new page, go to next step once you've found one.
  // FB will throttle my app if you make too many api calls. Do this one slow while testing.
  var newPage = {};
  var checkStep3 = function(){
    if (whichStep >= 3 && loggedIn){
      
      FB.api('/me/accounts/', function(response) {
        if (debug){
          console.log('Number of existing pages: ', numOfExistingPages);
          console.log('My accounts: ', response);
          if(numOfExistingPages>0){ // WHile testing, if no pages, then wait till they make one.
            var link3Html = $('#link3').html();
            newPage = response.data[0]; // While testing, use an exisiting page if there is one.
            link3Html = link3Html + "Debug mode: Using "+response.data[0].name;
            $('#link3').html(link3Html);
            clearInterval(t3);
            if (whichStep == 3){
              $('html, body').delay(5000).animate({ scrollTop: $('#link4').offset().top - body_padding }, 1000);
            }
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
  var t3 = setInterval(checkStep3,fb_request_time);

  // Once they add a description or a website, go to next step.
  var checkStep4 = function(){
    if (whichStep >= 4 && loggedIn){
      var stepComplete = false;
      FB.api(newPage.id, function(response) {
        if (debug){
          console.log('Page:');
          console.log(response);
          //clearInterval(t4); // Uncomment if your testing further steps. 
        }
        
        if(response.hasOwnProperty('about')){
          if(debug){
            console.log(response.about);
          }
          var link4Html = $('#link4').html();
          link4Html = link4Html + '<br/>You gave ' + newPage.name;
          link4Html = link4Html + ' a description of ' + response.about;
          $('#link4').html(link4Html);
          stepComplete = true;
        }

        if(response.hasOwnProperty('website')){
          if(debug){
            console.log(response.website);
          }
          var link4Html = $('#link4').html();
          link4Html = link4Html + '<br/> and set the website to: ' + response.website;
          $('#link4').html(link4Html);
          stepComplete = true;
        }
        
        if (whichStep == 4 && stepComplete){
          clearInterval(t4);
          $('html, body').delay(5000).animate({ scrollTop: $('#link5').offset().top - body_padding }, 1000);
        }
      });

    }
  }
  var t4 = setInterval(checkStep4,fb_request_time);

  // Once they add a picture, go to next step.
  var checkStep5 = function(){
    if (whichStep >= 5 && loggedIn){
      FB.api(newPage.id + '/picture', function(response) {
        if (debug){
          console.log('Picture:', response);
          console.log(response.data.is_silhouette);
          clearInterval(t5);
        }
        if(!response.data.is_silhouette){
          clearInterval(t5);
          setTimeout(function(){
            var link5Html = $('#link5').html();
            link5Html = link5Html + '<br/>What a nice picture';
            $('#link5').html(link5Html);
          }, 2000);
          if (whichStep == 5){
            $('html, body').delay(5000).animate({ scrollTop: $('#link6').offset().top - body_padding }, 1000);
          }
        }
      });
    }
  }
  var t5 = setInterval(checkStep5,fb_request_time);

});