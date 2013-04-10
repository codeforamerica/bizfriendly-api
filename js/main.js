var width = window.screen.width;
var height = window.screen.height;

var challengeSiteFeatures = {
	height: height,
    width: width*0.695,
    center:false
}

var instructionSiteFeatures = {
	height: height,
    width: width*0.305,
    left: width*0.695,
    center:false,
    name: 'How To City: Promotoe Your Business Online', // specify custom name for window (overrides createNew option)
}

$("#launch").click(function() {
  $.popupWindow('http://facebook.com', challengeSiteFeatures);
  $.popupWindow('facebook_instructions.html', instructionSiteFeatures);
});

 $('.navbar ul li a').bind('click', function(e) {
           e.preventDefault();
           $('html, body').animate({ scrollTop: $(this.hash).offset().top }, 300);

           // edit: Opera requires the "html" elm. animated
        });
