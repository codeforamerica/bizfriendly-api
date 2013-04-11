var width = window.screen.width;
var height = window.screen.height;

var challengeSiteFeatures = {
	height: height,
    width: width*0.695,
    center:false,
    name:'challenge'
}
console.log(challengeSiteFeatures);

var instructionSiteFeatures = {
	height: height,
    width: width*0.305,
    left: width*0.695,
    center:false,
    name: 'How To City: Promotoe Your Business Online', // specify custom name for window (overrides createNew option)
}

$("#launch").click(function() {
  $.popupWindow('facebook_instructions.html', instructionSiteFeatures);
});

$("#fb_pages").click(function() {
  $.popupWindow('https://www.facebook.com/pages/create/', challengeSiteFeatures);
});

 $('.navbar ul li a').bind('click', function(e) {
           e.preventDefault();
           $('html, body').animate({ scrollTop: $(this.hash).offset().top }, 300);

           // edit: Opera requires the "html" elm. animated
        });

var next;
$('.next').click(function() {
   if ( next === undefined ) {
     next = $('section').next();
     console.log(next);
   } else {
      next = next.next();
   }
   $('html, body').animate({ scrollTop: next.offset().top - 200 }, 300);
});

              // Additional JS functions here
              window.fbAsyncInit = function() {
                FB.init({
                  appId      : '158953284268352', // App ID
                  channelUrl : 'http://ondrae.github.io/howtocity/channel.html', // Channel File
                  status     : true, // check login status
                  cookie     : true, // enable cookies to allow the server to access the session
                  xfbml      : true  // parse XFBML
                });

                function login() {
                    FB.login(function(response) {
                        if (response.authResponse) {
                            // connected
                            testAPI();
                            FB.getLoginStatus;

                        } else {
                            // cancelled
                        }
                    });
                }

                function testAPI() {
                    console.log('Welcome!  Fetching your information.... ');
                    FB.api('/me', function(response) {
                        console.log('Good to see you, ' + response.name + '.');
                    });
                }

                FB.getLoginStatus(function(response) {
                  if (response.status === 'connected') {
                    // connected
                    console.log('Connected');
                    $('#link1').delay(1000).html('<h2>You\'re already logged into Facebook.</h2>');
                    $('html, body').delay(1000).animate({ scrollTop: $('#link2').offset().top }, 1000);
                  } else if (response.status === 'not_authorized') {
                    // not_authorized
                    console.log('not_authorized');
                    login();
                  } else {
                    // not_logged_in
                    console.log('not_logged_in');
                    login();
                  }
                 });


                // Additional init code here

              };

              // Load the SDK Asynchronously
              (function(d){
                 var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
                 if (d.getElementById(id)) {return;}
                 js = d.createElement('script'); js.id = id; js.async = true;
                 js.src = "//connect.facebook.net/en_US/all.js";
                 ref.parentNode.insertBefore(js, ref);
               }(document));

              $(document).scroll(function(){
              var theDistance =  $(window).scrollTop(),
                    theHeight = $(document).height(),
                heightPercent = theDistance/theHeight*100;

                console.log(Math.ceil(heightPercent));
                $('.bar').css('width',Math.ceil(heightPercent)+'%');

              });
