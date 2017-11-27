    $('.thumbnail').on({
        mousemove: function(e) {
            var $this = $(this);
            var offset = $this.offset();
            var width = $this.width();
            var height = $this.height();
            var centerX = offset.left + width / 2;
            var centerY = offset.top + height / 2;
            $(this).next('img').css({
            top:centerY-100,
            left:centerX-600});
    },
    mouseenter: function() {
        var big = $('<img />', {'class': 'thumbnail-big', src: this.src});
        $(this).after(big);
    },
    mouseleave: function() {
        $('.thumbnail-big').remove();
    }
});

$(document).ready(function () {
    document.getElementById('interval_field').style.display = 'none';
    $('select[name="action"]').change(function() {
    	if ($(this).val() == "set_periodic_scan") document.getElementById('interval_field').style.display = 'inline';
	else document.getElementById('interval_field').style.display = 'none';
    });
});
/*$(document).ready(function () {*/
/*    $($($("span.badge-forensic").closest("a").closest("th"))).attr("id","forensic");*/
/*    $($($("span.badge-non-forensic").closest("a").closest("th"))).attr("id","non-forensic");*/
/*});*/

function togglePassword(){
   var p = document.getElementById('id_email_password');
   if(p.getAttribute('type')=='password'){
   	p.setAttribute('type', 'text');
   	$('.icon-eye-open').removeClass('icon-eye-open').addClass('icon-eye-close');
   }
   else{
	p.setAttribute('type', 'password');
   	$('.icon-eye-close').removeClass('icon-eye-close').addClass('icon-eye-open');
   }
}
