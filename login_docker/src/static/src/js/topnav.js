$(document).ready(function(){
$(document).on('click', function(e){
    $('#topnav-menu').fadeOut();    
})
$('#topnav-menu-dropdown').on('click', function(e){
    e.stopPropagation();
    $('#topnav-menu').fadeToggle();
})
})