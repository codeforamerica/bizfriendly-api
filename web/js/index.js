var width = window.screen.width;
var height = window.screen.height;



var instructionSiteFeatures = {
  height: height,
  width: width*0.305,
  left: width*0.695,
  name: 'instructions', // specify custom name for window (overrides createNew option)
  center: false,
  // scrollbars: false, // safari always adds scrollbars
}

$("#launch").click(function() {
  // var challengeWindow = $.popupWindow('http://facebook.com', challengeSiteFeatures);
  var instructionsWindow = $.popupWindow('fb_page_instructions.html', instructionSiteFeatures);

  // instructionsWindow.onblur = function(){

  //   var t = setTimeout(function(){
  //     instructionsWindow.close();
  //     $.popupWindow('fb_page_instructions.html#link2', instructionSiteFeatures);
  //   }
  //     , 2000);
  //   // $.popupWindow('fb_page_instructions.html#link2', instructionSiteFeatures)
  //   instructionsWindow.onblur = function(){
  //     var t = setTimeout(function(){
  //       instructionsWindow.close();
  //       $.popupWindow('fb_page_instructions.html#link3', instructionSiteFeatures);
  //     }
  //     , 2000);
  //   }
  // }     

});
