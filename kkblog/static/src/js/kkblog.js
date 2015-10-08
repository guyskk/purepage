$(document).ready(function() {

    //导航条
    $(".head-nav-toggle").click(function() {
        $(".head-nav").slideToggle(150);
    });

    var searchbox_space = window.innerWidth - $(".head-title").outerWidth(true) - $(".head-nav-toggle").outerWidth(true) - $(".search-btn").outerWidth(true) - 60;
    $(".search-box").animate({
        width: (searchbox_space + "px")
    });
    if (searchbox_space < 125) {
        $(".search-box").focus(function() {
            $(".head-nav-toggle").hide();
            $(".search-box").animate({
                width: (searchbox_space + $(".head-nav-toggle").outerWidth(true)) + "px"
            });
        });
        $(".search-box").blur(function() {
            $(".search-box").animate({
                width: searchbox_space + "px"
            }, function() {
                $(".head-nav-toggle").show();
            });
        });
    }

    var head_offset = $(".head").height();
    var foot_offset = $(document).height() - window.innerHeight - 60;
    $(document).scroll(function() {
        var scrollTop = $(document).scrollTop();
        //侧边栏
        if (scrollTop < head_offset) {
            $(".side").removeClass("side-nohead");
        } else {
            $(".side").addClass("side-nohead");
        }
        if (scrollTop > foot_offset) {
            $(".side").removeClass("side-nofoot");
        } else {
            $(".side").addClass("side-nofoot");
        }

    });

    //只作用于宽度<=768px的article页面
    if (window.innerWidth <= 768 && $(".article").length > 0) {
        var article_offset = $(".head").height() + $(".article").height() - 0.5 * window.innerHeight;
        //侧边栏小按钮（目录）
        $(document).scroll(function() {
            var scrollTop = $(document).scrollTop();
            if (scrollTop > head_offset && scrollTop < article_offset) {
                $(".side-toggle").show();
            } else {
                $(".side-toggle").hide();
                $(".side").hide();
                $(".side-toggle").text("目录");
            }
        });

        //侧边栏（目录）
        $(".side-toggle").click(function() {
            $(".side").toggle();
            if ($(".side").is(":visible")) {
                $(".side-toggle").text("X");
            } else {
                $(".side-toggle").text("目录");
            }
        });

        //点击后关闭侧边栏
        $(".side-outline a").click(function(event) {
            $(".side").fadeOut(150);
            $(".side-toggle").text("目录");
        });
    }
});
