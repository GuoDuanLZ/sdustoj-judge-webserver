/**
 * Created by zzk on 16-8-22.
 */
    $(function () {
        var meta_id=$('#meta_id_hidden').text();
        var id=$('#id_hidden').text();
              $.ajax({
                url: "/api-server/meta-problems/"+meta_id+"/descriptions/",
                type: "GET",
                dataType: "json",
                data: {
                },
                success: function (response) {

                     $.each(response.results,function (i,item) {
                       $('#description').append(function(){
                           var op='<option value="'+item.id+'">'+item.title+'</option>'
                           return op;
                       });
                    });
                },
                error: function (response) {
                    console.log(response);
                }

            });
              $.ajax({
                url: "/api-server/meta-problems/"+meta_id+"/samples/",
                type: "GET",
                dataType: "json",
                data: {
                },
                success: function (response) {

                     $.each(response.results,function (i,item) {
                       $('#sample').append(function(){
                           var op='<option value="'+item.id+'">'+item.title+'</option>'
                           return op;
                       });
                    });
                },
                error: function (response) {
                    console.log(response);
                }

            });
            $.ajax({
                url: "/api-server/meta-problems/"+meta_id+"/problems/"+id+"/",
                type: "GET",
                dataType: "json",
                data: {
                },
                success: function (response) {
                    $('#title').val(response.title);
                    $('#author').val(response.author);
                    $('#source').val(response.source);
                    $('#introduction').val(response.introduction);
                    $('#status option').each(function (i,item) {
                        var op=$(this).val();
                        if(op==response.status)
                            $(this).prop('selected','selected');
                    });
                    $('#test_type option').each(function (i,item) {
                        var op=$(this).val();
                        if(op==response.test_type)
                            $(this).prop('selected','selected');
                    });
                    $('#description option').each(function (i,item) {
                        var op=$(this).val();
                        if(op==response.description)
                            $(this).prop('selected','selected');
                    });
                    $('#sample option').each(function (i,item) {
                        var op=$(this).val();
                        if(op==response.sample)
                            $(this).prop('selected','selected');
                    });
                },
                error: function (response) {
                    console.log(response);
                }

            });
        $('#maketrue').click(function () {
          $.ajax({
                url: "/api-server/meta-problems/"+meta_id+"/problems/"+id+'/',
                type: "PATCH",
                dataType: "json",
                data: {
                    title:$('#title').val(),
                    author:$('#author').val(),
                    source:$('#source').val(),
                    introduction:$('#introduction').val(),
                    status:$('#status').prop('value'),
                    test_type:$('#test_type').prop('value'),
                    description:$('#description').prop('value'),
                    sample:$('#sample').prop('value'),
                },
                success: function (response) {
                    alert('修改成功');
                    location.href='/problem-detail?id='+meta_id;
                },
                error: function (response) {
                    console.log(response);
                }

            });
        });


    });

