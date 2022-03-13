function getContracts(client_id) {
    let $ = django.jQuery;
    $.get('/get/contracts/' + client_id, function (resp){

        let contract_list = '<option value="" selected="">---------</option>'
        $.each(resp.data, function(i, item){
           contract_list += '<option value="'+ item.id +'">'+ item.name +'</option>'
        });
        $('#id_contract').html(contract_list);
    });
}


function getSales(client_id) {
    let $ = django.jQuery;
    $.get('/get/sales/' + client_id, function (resp){

        let sales_list = '<option value="" selected="">---------</option>'
        $.each(resp.data, function(i, item){
           sales_list += '<option value="'+ item.id +'">'+ item.name +'</option>'
        });
        $('#id_sales').html(sales_list);
    });
}
