$(document).ready(
    (function($) {
    var element = $('.follow-scroll')

    if (element.length) {
        var originalY = element.offset().top;
        // Space between element and top of screen (when scrolling)
        var topMargin = 30;
        
        $(window).on('scroll', function(event) {
            var scrollTop = $(window).scrollTop();
            
            element.stop(false, false).animate({
                top: scrollTop < originalY
                        ? 0
                        : scrollTop - originalY + topMargin
            }, 300);
        });
    }
    
}));