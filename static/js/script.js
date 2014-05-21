/**
 * Created by vitalijlogvinenko on 02.05.14.
 */
$(document).ready(function(){
    $('select.select_cat').change(function(){
        var cat_id = $(this).val();
        window.location = '/'+cat_id+'/1/';
    });
    $.ajaxSetup({
      data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
    });
    $.ajax({
        type: "POST",
        url: "/1/1/",
        data: {
            cat_id: 1,
            page: 1,
            csrfmiddlewaretoken: $('.stockhunter-table #csrf-token').text()
        },
        dataType: "json",
        cache: false,
        success: function(response){
            console.log(response);
        }
    });

});
