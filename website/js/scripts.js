/*
/*

/**

/* ** Anchor Slider by Cedric Dugas **
* Copyright (c) 2012 Cedric Dugas, http://www.position-absolute.com/
* via
* https://github.com/posabsolute/jquery-scrollbar-slider ** */

$(document).ready(function() {
        $("a.anchorLink").anchorAnimate()
});

jQuery.fn.anchorAnimate = function(settings) {

        settings = jQuery.extend({
                speed : 1100
        }, settings);	

        return this.each(function(){
                var caller = this
                $(caller).click(function (event) {	
                        event.preventDefault()
                        var locationHref = window.location.href
                        var elementClick = $(caller).attr("href")

                        var destination = $(elementClick).offset().top;
                        $("html:not(:animated),body:not(:animated)").animate({ scrollTop: destination}, settings.speed, function() {
                                window.location.hash = elementClick
                        });
                        return false;
                })
        })
}

function toggleDiv(divId) {
   $("#"+divId).toggle('500',"linear");
}