/**
 * Created by vitalijlogvinenko on 02.05.14.
 */
$(document).ready(function(){
    $('select.select_cat').change(function(){
        var cat_id = $(this).val();
        window.location = '/'+cat_id+'/1/';
    });
    $.ajax({
        type: "POST",
        url: "/getTableData/",
        data: {
            cat_id: 1,
            page: 1,
            csrfmiddlewaretoken: $('.stockhunter-table #csrf-token').text()
        },
        dataType: "json",
        cache: false,
        success: function(response){
            renderTable(response)
        }
    });

});

function renderTable(data){
    var systems = data['systems'],
        tickers = data['tickers'];
    console.log(data);
    thSystems = ''; //Заголовки таблицы
    bodyTickers = ''; //Тело таблицы

    //Формируем строку с заголовком с системами
/*    for( i=0; i<systems.length; i++ ){
        thSystems += "<th>"+
            systems[i]['name'] +
            "</th>";
    }*/

    //Формируем строку <tbody>
    for( i=0; i<tickers.length; i++ ){
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

    $('.table-ajax .table').append(
        "<tbody>" +
        bodyTickers +
    "</tbody>");
}
