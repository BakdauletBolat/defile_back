function getSubCategory(category_id) {
    let $ = django.jQuery;
    $.get('/ajax/get_subcategory/' + category_id, function (resp){
        let kecamatan_list = '<option value="" selected="">---------</option>'
        $.each(resp.data, function(i, item){
           kecamatan_list += '<option value="'+ item.id +'">'+ item.name +'</option>'
        });
        $('#id_subcategory').html(kecamatan_list);
    });
}