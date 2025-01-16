(function ($) {
    "use strict";

    /**
     * 
     * Blog Slider
     */
    var blog_slider_script_js = function ($scope, $) {

        /* Brand */
        const element = $scope.find('.blog__slider');
        let data_settings = element.data('blog-slide-settings');
        const swiper_init = '.resources_slider_' + data_settings.slider_wrapper;
        const slide_next = '.next_' + data_settings.slider_wrapper;
        const slide_prev = '.prev_' + data_settings.slider_wrapper;

        // desktop
        let slide_des = data_settings.blog_slide_column.d ?? 3;
        let slide_teb = data_settings.blog_slide_column.t ?? 2;
        let slide_mob = data_settings.blog_slide_column.m ?? 1;

        let auto_play = data_settings.slide_auto_play ? {
            delay: data_settings.slide_auto_play_speed
        } : false;

        var resourcesSlider = new Swiper(swiper_init, {
            spaceBetween: data_settings.slide_space,
            loop: true,
            autoplay: auto_play,
            speed: data_settings.slide_speed,
            breakpoints: {
                480: {
                    slidesPerView: slide_mob
                },
                768: {
                    slidesPerView: slide_teb
                },
                992: {
                    slidesPerView: slide_teb
                },
                1200: {
                    slidesPerView: slide_des
                },
            },
            navigation: {
                nextEl: slide_next,
                prevEl: slide_prev,
            },
        });

    }
    $(window).on('elementor/frontend/init', function () {
        elementorFrontend.hooks.addAction('frontend/element_ready/powerai_blog_slider.default', blog_slider_script_js);
    });


    /**
     * 
     * Brans Carousel
     */
    var banner_carousel_script_js = function ($scope, $) {

        /* Brand */
        var brand_slider = new Swiper('.brand-slide-wrap', {
            spaceBetween: 100,
            centeredSlides: true,
            speed: 5000,
            autoplay: {
                delay: 1,
            },
            loop: true,
            slidesPerView: 'auto',
            allowTouchMove: false,
            disableOnInteraction: true,
            breakpoints: {
                320: {
                    spaceBetween: 50,
                },
                992: {
                    spaceBetween: 70,
                }
            },
        });
    }
    $(window).on('elementor/frontend/init', function () {
        elementorFrontend.hooks.addAction('frontend/element_ready/powerai_carousel.default', banner_carousel_script_js);
    });


    /**
     * 
     * Brans Carousel
     */
    var testimonial_slider_script_js = function ($scope, $) {

        const element = $scope.find('.pai__testimonial');
        let data_settings = element.data('testimonial-slide-settings');

        if (data_settings.slider_style == 1) {
            const swiper_init = '.testimonial__slider_' + data_settings.slider_wrapper;

            var testimonial_slider = new Swiper(swiper_init, {
                spaceBetween: data_settings.slide_space,
                centeredSlides: true,
                speed: data_settings.slide_speed,
                autoplay: {
                    delay: 1,
                    reverseDirection: data_settings.reverse_slider
                },
                loop: true,
                slidesPerView: 'auto',
                allowTouchMove: false,
                disableOnInteraction: true
            });
        } else if (data_settings.slider_style == 2 || data_settings.slider_style == 3) {
            // const swiper_init = '.testimonial__slider_' + data_settings.slider_wrapper;
            // Testimonial Image Generator
            var testimonialImg = new Swiper('.testimonial-img-slide', {
                fadeEffect: { crossFade: true },
                effect: 'fade',
                loop: true,
                allowTouchMove: false,
            })

            var testimonialInfo = new Swiper('.testimonial-info-slide', {
                spaceBetween: 24,
                slidesPerView: 1,
                loop: true,
                speed: 800,
                allowTouchMove: false,
                navigation: {
                    nextEl: ".testimonial-info-button-next",
                    prevEl: ".testimonial-info-button-prev",
                },
                pagination: {
                    el: ".testimonial-info-pagination",
                    clickable: true,
                },
                thumbs: {
                swiper: testimonialImg
                }
            });

            /* Testimonial End */
        } else if (data_settings.slider_style == 3 || data_settings.slider_style == 4) {
            var cg_testimonialSlider = new Swiper('.cg-testimonial-slide', {
                slidesPerView: 3,
                spaceBetween: 15,
                loop: true,
                speed: 1000,
                breakpoints: {
                    320: {
                        slidesPerView: 1
                    },
                    480: {
                        slidesPerView: 1
                    },
                    768: {
                        slidesPerView: 2
                    },
                    992: {
                        slidesPerView: 2
                    },
                    1200: {
                        slidesPerView: 3
                    },
                    1400: {
                        slidesPerView: 3
                    }
                },
                navigation: {
                    nextEl: ".cg-testimonial-info-button-next",
                    prevEl: ".cg-testimonial-info-button-prev",
                },
                pagination: {
                    el: ".cg-testimonial-info-pagination",
                    clickable: true,
                },
            });
        }

    }
    $(window).on('elementor/frontend/init', function () {
        elementorFrontend.hooks.addAction('frontend/element_ready/powerai_testimonial_slider.default', testimonial_slider_script_js);
    });


    /**
     * 
     * PowerAI Counter
     */
    var powerai_counter_script_js = function ($scope, $) {

        ///////////////////////////////////////////////////////
        // Odometer Counter
        $(".counter-item").each(function () {
            $(this).isInViewport(function (status) {
                if (status === "entered") {
                    for (var i = 0; i < document.querySelectorAll(".odometer").length; i++) {
                        var el = document.querySelectorAll('.odometer')[i];
                        el.innerHTML = el.getAttribute("data-odometer-final");
                    }
                }
            });
        });
    }
    $(window).on('elementor/frontend/init', function () {
        elementorFrontend.hooks.addAction('frontend/element_ready/powerai_counter.default', powerai_counter_script_js);
    });

    /**
    * 
    * PowerAI Pricing Filtarable gallery
    */
    var powerai_filterable_gallery_script_js = function ($scope, $) {

        ///////////////////////////////////////////////////////
        //Mixitup
        $('.work-mixi').mixItUp();

    }
    $(window).on('elementor/frontend/init', function () {
        elementorFrontend.hooks.addAction('frontend/element_ready/powerai_filterable_gallery.default', powerai_filterable_gallery_script_js);
    });

    /**
     * 
     * PowerAI Pricing Table
     */
    var powerai_pricing_table_script_js = function ($scope, $) {

        // Pricing Toggle
        const tableWrapper = document.querySelector(".price_wrapper");
        const switchInputs = document.querySelectorAll(".switch-wrapper input");
        const prices = tableWrapper?.querySelectorAll(".price");
        const toggleClass = "hide";

        for (const switchInput of switchInputs) {
            switchInput.addEventListener("input", function () {
                for (const price of prices) {
                    price.classList.add(toggleClass);
                }
                const activePrices = tableWrapper.querySelectorAll(
                    `.price.${switchInput.id}`
                );
                for (const activePrice of activePrices) {
                    activePrice.classList.remove(toggleClass);
                }
            });
        }
        // Pricing Toggle End
    }
    $(window).on('elementor/frontend/init', function () {
        elementorFrontend.hooks.addAction('frontend/element_ready/powerai_pricing_table.default', powerai_pricing_table_script_js);
    });


})(window.jQuery);