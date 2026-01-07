$(function() {
  "use strict";

  //------- Parallax -------//
  skrollr.init({
    forceHeight: false
  });

  //------- Active Nice Select --------//
  $('select').niceSelect();

  //------- hero carousel -------//
  $(".hero-carousel").owlCarousel({
    items:3,
    margin: 10,
    autoplay:false,
    autoplayTimeout: 5000,
    loop:true,
    nav:false,
    dots:false,
    responsive:{
      0:{
        items:1
      },
      600:{
        items: 2
      },
      810:{
        items:3
      }
    }
  });

  //------- Best Seller Carousel -------//
  if($('.owl-carousel').length > 0){
    $('#bestSellerCarousel').owlCarousel({
      loop:true,
      margin:30,
      nav:true,
      navText: ["<i class='ti-arrow-left'></i>","<i class='ti-arrow-right'></i>"],
      dots: false,
      responsive:{
        0:{
          items:1
        },
        600:{
          items: 2
        },
        900:{
          items:3
        },
        1130:{
          items:4
        }
      }
    })
  }

  //------- single product area carousel -------//
  $(".s_Product_carousel").owlCarousel({
    items:1,
    autoplay:false,
    autoplayTimeout: 5000,
    loop:true,
    nav:false,
    dots:false
  });

  //------- mailchimp --------//  
	function mailChimp() {
		$('#mc_embed_signup').find('form').ajaxChimp();
	}
  mailChimp();
  
  //------- fixed navbar --------//  
  $(window).scroll(function(){
    var sticky = $('.header_area'),
    scroll = $(window).scrollTop();

    if (scroll >= 100) sticky.addClass('fixed');
    else sticky.removeClass('fixed');
  });

  if (document.getElementById("price-range")) {

    var slider = document.getElementById("price-range");

    var minInput = document.getElementById("preco_min");
    var maxInput = document.getElementById("preco_max");

    var lowerValue = document.getElementById("lower-value");
    var upperValue = document.getElementById("upper-value");

    noUiSlider.create(slider, {
        start: [
            parseInt(minInput.value),
            parseInt(maxInput.value)
        ],
        connect: true,
        range: {
            min: 0,
            max: 10000
        },
        step: 50
    });

    slider.noUiSlider.on("update", function (values) {
        lowerValue.innerHTML = Math.round(values[0]);
        upperValue.innerHTML = Math.round(values[1]);

        minInput.value = Math.round(values[0]);
        maxInput.value = Math.round(values[1]);
    });

    slider.noUiSlider.on("end", function () {
        document.getElementById("filtros").submit();
    });
}

  
});

