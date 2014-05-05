/**
 * Created by vitalijlogvinenko on 02.05.14.
 */
$(document).ready(function(){
    $('select.select_cat').change(function(){
        var cat_id = $(this).val();
        window.location = '/stock/'+cat_id+'/1/';
    });

});
