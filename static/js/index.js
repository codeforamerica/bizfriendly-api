var width = window.screen.width;
var height = window.screen.height;

var instructionSiteFeatures = {
  height: height,
  width: width - 1000,
  left: 1000,
  name: 'instructions', // specify custom name for window (overrides createNew option)
  center: false,
  // scrollbars: false, // safari always adds scrollbars
}

$("#launch").click(function() {
  var instructionsWindow = $.popupWindow('fb_page_instructions.html', instructionSiteFeatures);
});
