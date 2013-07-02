var debug = true;
var request_time = 2000;

// UI ----------------------------------------------------------------------------------------
// Scroll bar and which step

//Fix width
var width = window.screen.width;
$('.narrow').css('width',280); // Hackity

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

// Steps Functions ----------------------------------------------------------------------------------------
  
var checkStep1 = function(){
  if (whichStep > 1){
    clearInterval(t1);
  }
  if (whichStep == 1){
    if ($('#link1 .feedback').css('display') != 'none'){
      $('html, body').delay(3000).animate({ scrollTop: $('#link2').offset().top - body_padding }, 1000);
    }
  }
}
  
var t1 = setInterval(checkStep1,1000);

// When we get to step 2, open up the challenge window
  var width = window.screen.width;
  var height = window.screen.height;
  var challengeSiteFeatures = {
    height: height,
    width: 1000,
    name: 'challenge',
    center: false
  }
  var challengeWindow = false;
  $("#open_foursquare").click(function(){
    challengeWindow = $.popupWindow('https://www.foursquare.com', challengeSiteFeatures);
    setTimeout(function(){
      // Show the feedback
      $('#link2 .feedback').toggle();
    }, 1000);
    if (whichStep == 2){
      $('html, body').delay(3000).animate({ scrollTop: $('#link3').offset().top - body_padding }, 1000); 
    }
  })

  $("#foursquare_yes").click(function(){
    $('#link3 .feedback').toggle();
    $('#link3 .feedback .yes').toggle();
  })


  $("#foursquare_claim_venue").click(function(){
    $('#link3 .feedback').append('<h3>Goodbye.</h3>')
    setTimeout(function(){
      challengeWindow.close();
      window.close();
    }
      ,2000);
  })

  $("#foursquare_no").click(function(){
    $('#link3 .feedback').toggle();
    $('#link3 .feedback .no').toggle();
  })

  $('#foursquare_create_venue').click(function(){
    challengeWindow = $.popupWindow('https://foursquare.com/add_venue', challengeSiteFeatures);
    $('html, body').delay(3000).animate({ scrollTop: $('#link4').offset().top - body_padding }, 1000); 
  })

var thirdSiteFeatures = {
    height: height,
    width: 1000,
    name: 'third',
    center: false
  }

$('#foursquare_style_guide').click(function(){
  console.log('style guide btn');
    thirdWindow = $.popupWindow('http://aboutfoursquare.com/style-guide/', thirdSiteFeatures);
    $('#foursquare_style_guide').toggle();
    $('#close_style_guide').toggle();
  })
  
  $('#close_style_guide').click(function(){
  thirdWindow.close();
  $('#close_style_guide').toggle();
  $('#foursquare_style_guide').toggle();
  })