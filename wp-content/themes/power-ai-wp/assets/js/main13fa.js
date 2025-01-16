(function($) {
    "use strict";



    $(document).ready(function() {

        $(window).on('scroll', (function() {


            ///////////////////////////////////////////////////////
            // Bottom to top start
            if ($(this).scrollTop() > 100) {
                $('#scroll-top').fadeIn();
            } else {
                $('#scroll-top').fadeOut();
            }
            // Bottom to top end


            //on scroll end
        }));


        $('#scroll-top').on('click', function() {
            $("html, body").animate({
                scrollTop: 0
            }, 600);
            return false;
        });
        // Bottom to top End

        // Menu
        jQuery('header .mainmenu').meanmenu({
            meanScreenWidth: "1199",
        });

    });



    $(window).on('load', () => {
        // Preloader
        $('.preloader').fadeOut("slow");
        // Preloader End

        // Custom Cursor
        const cursor = document.querySelector('.cursor');
        if (cursor) {
            const editCursor = e => {
                const {
                    clientX: x,
                    clientY: y
                } = e;
                cursor.style.left = x + 'px';
                cursor.style.top = y + 'px';
            };
            window.addEventListener('mousemove', editCursor);

            document.querySelectorAll("a, .cursor-pointer").forEach(item => {
                item.addEventListener('mouseover', () => {
                    cursor.classList.add('cursor-active');
                });

                item.addEventListener('mouseout', () => {
                    cursor.classList.remove('cursor-active');
                });
            });
        }
        // Custom Cursor end

    })




    document.querySelectorAll('.menu-anim > li > a').forEach(button => button.innerHTML = '<div class="menu-text"><span>' + button.textContent.split('').join('</span><span>') + '</span></div>');

    setTimeout(() => {
        var menu_text = document.querySelectorAll(".menu-text span");
        menu_text.forEach((item) => {
            var font_sizes = window.getComputedStyle(item, null);
            let font_size = font_sizes.getPropertyValue("font-size");
            let size_in_number = parseInt(font_size.replace("px", ""), 10);
            let new_size = parseInt(size_in_number / 3, 10);
            new_size = new_size + "px";
            if (item.innerHTML === " ") {
                item.style.width = new_size;
            }
        });
    }, 1000);

    // Menu End


    $('.popup-youtube').magnificPopup({
        type: 'iframe'
    });


    /* init swipper slider */
    var swiper = new Swiper(".blog_thumb__slider", {
        spaceBetween: 0,
        loop: true,
        effect: "fade",
        fadeEffect: {
            crossFade: true
        },
        navigation: {
            nextEl: ".blog-button-next",
            prevEl: ".blog-button-prev",
        },
        pagination: false
    });

    // Magnific Popup gallery End


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

    /* Brand End */

}(jQuery));