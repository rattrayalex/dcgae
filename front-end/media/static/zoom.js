var selectors = ["img#left_img", "img#right_img"]

$(document).ready(function() {
	dczoom();
});

function dczoom() {
    $(selectors.join(",")).hover(function (e) {
        var image = $(this).attr("src");
				if (image.match(/\d\/med$/)) {
					image = image.replace(/\/med$/, "/full");	
				} else {
					image = image.replace(/\/med$/, "/full");
				}
				//var title = $(this).attr("alt") || $(this).attr("title");
				hover_timer = setTimeout(function() {
					$("body").prepend('<div id="dczoom"><img src="' + image + '" /></div>');
					//if (title.length > 0) {
					//	$("#dczoom").append("<p>"+title+"</p>");
					//}
					position_dczoom(e);
				},250);
    }, function () {
        $("#dczoom").remove();
				clearTimeout(hover_timer);
    });
	
    $("img").mousemove(function (e) {
				position_dczoom(e);
    });
}

function position_dczoom(e) {
	iheight = $("#dczoom img").height();
  iwidth = $("#dczoom img").width();
  if ($(window).scrollTop() + 20 >= e.pageY - iheight) {
      $("#dczoom").css("top", (e.pageY - 10) + "px")
  } else {
      $("#dczoom").css("top", (e.pageY - iheight - 10) + "px")
  }
  if ($(window).width() - 20 >= e.pageX + iwidth) {
      $("#dczoom").css("left", (e.pageX + 30) + "px");
  } else {
      $("#dczoom").css("left", (e.pageX - 30 - iwidth) + "px");
  }
}