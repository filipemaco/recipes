$( document ).ready(function() {

    let hide_ingredients = false;

    $( "#ingredients .ingredient_card" ).each(function( count ) {
        if (hide_ingredients) {
            $(this).hide();
        } else if (($("#ingredients-" + count + "-value").val())) {
            console.log("dsdasd")
        } else {
            hide_ingredients = true;
        }
        $("#ingredients-" + count + "-value").addClass("allownumericwithdecimal");
        $("#ingredients-" + count + "-unit_type").addClass("select2");
    });

    $( "#add_ingredient" ).click(function() {
        $("#ingredients .ingredient_card:hidden:first").show();
    });

    $ ( ".remove_ingredient" ).click(function() {
        const id = $(this).closest('.ingredient_card').data('id');
        $(this).closest('.ingredient_card').hide();
        $(this).closest('.ingredient_card').find("#ingredients-" + id + "-value").val('');
        $(this).closest('.ingredient_card').find("#ingredients-" + id + "-ingredient_name").val('');
    });

    if($("#edit_recipe").length == 1) {
        $( "#edit_recipe li" ).each(function( index ) {
            $(".ingredient_card").find("#ingredients-" + index + "-value").val($(this).data('value'));
            $(".ingredient_card").find("#ingredients-" + index + "-ingredient_name").val($(this).data('ingredient_name'));
            $(".ingredient_card").find("#ingredients-" + index + "-unit_type").val($(this).data('unit_type'));
            $(".ingredient_card[data-id='" + index + "']").show();
        });
    }

    $(".allownumericwithdecimal").on("keypress keyup blur",function (event) {
        //this.value = this.value.replace(/[^0-9\.]/g,'');
        $(this).val($(this).val().replace(/[^0-9\.]/g,''));
        if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
            event.preventDefault();
        }
    });

    $(".select2").select2();

    $(".select2-selection--single").addClass("height_38");

});