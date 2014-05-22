/**
 * Created by vitalijlogvinenko on 02.05.14.
 */
$(document).ready(function(){
    cat_id = $('select.select_cat').val();
    lastTicker = Number($('.table-ajax table tbody tr:last-child td.counter').text());
    updateTable(cat_id, lastTicker);

    $('select.select_cat').change(function(){
        var cat_id = $(this).val();
        window.location = '/'+cat_id;
    });

    $('.update-table').on("click", function(){
        cat_id = $('select.select_cat').val();
        lastTicker = Number($('.table-ajax table tbody tr:last-child td.counter').text());
        //updateTable(cat_id, lastTicker);
        response = JSON.parse($('.data').html());
        countTickers = response['tickers'].length;
        renderTable(response, lastTicker);
        lastTicker = Number($('.table-ajax table tbody tr:last-child td.counter').text());
        if(lastTicker>=countTickers){
            $('.update-table').hide();
        }
        else{
            $('.update-table').show();
        }
    });

});

function updateTable(cat_id, lastTicker){
    $('.update-table').hide();
    $('.update-preloader').show();
    $.ajax({
        type: "POST",
        url: "/getTableData/",
        data: {
            cat_id: cat_id,
            page: lastTicker,
            csrfmiddlewaretoken: $('.stockhunter-table #csrf-token').text()
        },
        dataType: "json",
        cache: false,
        success: function(response){
//            var a = response['tickers'].concat();
//            a = response['tickers'].slice(0);
            $('.data').html(JSON.stringify(response));
//            response['tickers'].length = 0;
//            for (i=0; i<51; i++){
//                response['tickers'].push(a[i]);
//            }
            console.log(response);
            renderTable(response, 0);
            if(!response['pageEnd'])
                $('.update-table').show();
            else
                $('.update-table').hide();
            $('.update-preloader').hide();
        }
    });
}

function renderTable(data, from){
    var systems = data['systems'],
        tickers = data['tickers'];
    thSystems = ''; //Заголовки таблицы
    bodyTickers = ''; //Тело таблицы

    //Формируем строку с заголовком с системами
/*    for( i=0; i<systems.length; i++ ){
        thSystems += "<th>"+
            systems[i]['name'] +
            "</th>";
    }*/
    //from = 0;
    //to = tickers.length;
    //Формируем строку <tbody>
    if(tickers.length-from>50){
        to = from + 50;
    }
    else{
        to = tickers.length;
    }
    for( i=from; i<to; i++ ){
        //tickers[i]['counter']
        htmlText = "<tr>" +
            "<td class='counter'> "+(i+1)+"</td>" +
            "<td>"+tickers[i]['name']+"</td>" +
            "<td>"+tickers[i]['last_update']+"</td>";
        for( j=0; j<systems.length; j++ ){
            htmlText += "<td>";
            signals = tickers[i]['signals'];
            for (var value in signals){
                if(value == systems[j]['identifer']){
                    if( signals[value].length > 0) {
                        for (k=0; k<signals[value].length; k++){
                            signal = signals[value][k];
                            if( signal['type'] == 'up' ){
                                htmlText += '&nbsp;<span style="color:green" title=' + signal["date"] + '>'+ signal['per'] + '</span>';
                            }
                            if( signal['type'] == 'down' ){
                                htmlText += '&nbsp;<span style="color:red" title=' + signal["date"] + '>'+ signal['per'] + '</span>';
                            }
                            if( signal['type'] == 'in' ){
                                htmlText += '&nbsp;<span style="color:black" title=' + signal["date"] + '>'+ signal['per'] + '</span>';
                            }
                        }
                    }
                }
            }
            htmlText += "</td>";
        }
        htmlText += "</tr>";
        bodyTickers += htmlText;
    }
    $('.table-ajax .table tbody').append(bodyTickers);
}
