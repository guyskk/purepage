/*! kkblog - v0.1.0 - 2015-07-30
* http://kkblog.me
* Copyright (c) 2015 ; Licensed  */
function add_head_one_row() {
    $(".head").addClass("head-one-row");
    $(".center").addClass("center-one-row");
    $(".side").addClass("side-one-row");
}

function remove_head_one_row() {
    $(".head").removeClass("head-one-row");
    $(".center").removeClass("center-one-row");
    $(".side").removeClass("side-one-row");
} 

$(document).ready(function() {
    $(document).scroll(function() {
        if ($(document).scrollTop() < 45) {
            remove_head_one_row();
        } else /* if (document.body.scrollTop < 120) */ {
            add_head_one_row();
        }
    });
});