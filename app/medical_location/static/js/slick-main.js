

$('.medical-card-slider').slick({
  centerMode: true,
  centerPadding: '60px',
  slidesToShow: 4,
  infinite: true,
  autoplay: true,
    //  prevArrow: none,
    //  nextArrow: none,
  responsive: [
    {
      breakpoint: 768,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '40px',
        slidesToShow: 3
      }
    },
    {
      breakpoint: 480,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '40px',
        slidesToShow: 1
      }
    }
  ]
});
