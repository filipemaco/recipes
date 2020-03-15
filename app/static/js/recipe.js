$( document ).ready(function() {

    let hide_ingredients = false;

    $( "#ingredients fieldset" ).each(function( count ) {
        $(this).find("legend").hide();

        if (hide_ingredients) {
            $(this).hide();
        } else if (($("#ingredients-" + count + "-value").val())) {
        } else {
            hide_ingredients = true;
        }
    });

    $( "#add_ingredient" ).click(function() {
        $("#ingredients fieldset:hidden:first").show();
    });

});