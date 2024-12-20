(function ($) {
  "use strict";

  /*============= preloader js css =============*/
  var cites = [];
  cites[0] = "Unlock financial wisdom and take control of your money today";
  cites[1] = "Your daily dose of actionable insights for financial freedom awaits";
  cites[2] = "Read, learn, and grow smarter with every blog you explore";
  cites[3] = "Discover strategies to save, grow, and achieve financial success";
  cites[4] = "Transform your financial future—start with our daily expert insights";
  cites[5] = "Empowering you with knowledge to make smarter money decisions";
  cites[6] = "Stay informed, stay inspired—money tips you can't afford to miss";
  cites[7] = "Elevate your financial IQ—explore more blogs that matter now";
  cites[8] = "Practical advice to guide you toward your financial goals daily";
  cites[9] = "From savings to investments, master your money with us today";
  var cite = cites[Math.floor(Math.random() * cites.length)];
  $("#preloader p").text(cite);
  $("#preloader").addClass("loading");

  $(window).on("load", function () {
    setTimeout(function () {
      $("#preloader").fadeOut(500, function () {
        $("#preloader").removeClass("loading");
      });
    }, 500);
  });
})(jQuery);
