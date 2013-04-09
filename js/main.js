var width = window.screen.width;
var height = window.screen.height;

var challengeSiteFeatures = "width=1000,height="+height;
var instructionSiteFeatures = "width=440,height="+height+",left=1000";

$("#launch").click(function() {
  window.open("http://facebook.com","", challengeSiteFeatures);
  window.open("facebook_instructions.html","", instructionSiteFeatures);
});
