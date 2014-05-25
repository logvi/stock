/**
 * Created by vitalijlogvinenko on 23.05.14.
 */
$(document).ready(function(){
    $('button.upload-d').click(function(){
        uploadData('D');
    });
    $('button.upload-w').click(function(){
        uploadData('W');
    });
    $('button.upload-m').click(function(){
        uploadData('M');
    });
    $('.startPars').click(function(){
       parsData(false);
    });
    $('.loadPars').click(function(){
       catName = $('select.select_cat :selected').text();
       bootbox.confirm("Выгрузить тикеры в категорию " + catName + "?", function(result){
           if(result)
            parsData(true);
       });
    });
});
//Посылает запрос на сервер для загрузки данных
function uploadData(per){
    cat_id = $('select.select_cat').val();
    $('.update-preloader').show();
    $('.upload-data').hide();
    $.ajax({
        type: "POST",
        url: "/stock/upload/",
        data: {
            cat_id: cat_id,
            per: per,
            csrfmiddlewaretoken: $('.container-fluid #csrf-token').text()
        },
        dataType: "json",
        cache: false,
        success: function(response){
            console.log(response);
            $('.update-preloader').hide();
            $('.upload-data').show();
        }
    });
}

//Парсировка html
function parsData(saveInDB){
    parsString = $('.parsString').val();
    cat_id = $('select.select_cat').val();
    $.ajax({
        type: "POST",
        url: "/stock/parsing/",
        data: {
            parsString: parsString,
            saveInDB: saveInDB,
            catId: cat_id,
            csrfmiddlewaretoken: $('.container-fluid #csrf-token').text()
        },
        dataType: "json",
        cache: false,
        success: function(response){
            console.log(response);
            if(!saveInDB){
                text = '';
                for(i = 0; i<response['data'].length; i++){
                    text += 'id: '+response['data'][i]['id'] + '; value = ' + response['data'][i]['value'] + '\n';
                }
                $('.parsRes').val(text);
            }
            else{
                bootbox.alert(response['data']);
            }
        }
    });
}