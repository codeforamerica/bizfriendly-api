var width = window.screen.width;
var height = window.screen.height;

var challengeSiteFeatures = {
  height: height,
    width: width*0.695,
    center:false,
    name:'challenge'
}
// console.log(challengeSiteFeatures);

var instructionSiteFeatures = {
  height: height,
    width: width*0.305,
    left: width*0.695,
    center:false,
    name: 'How to City: Promote Your Business Online', // specify custom name for window (overrides createNew option)
}

$("#launch").click(function() {
  $.popupWindow('/challenge/facebook_page', instructionSiteFeatures);
});
