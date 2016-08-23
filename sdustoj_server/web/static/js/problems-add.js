/**
 * Created by zzk on 16-8-22.
 */
 $(function () {
    var meta_id=$('#meta_id_hidden').text();
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
        $('#maketrue').click(function () {
          $.ajax({
                url: "/api-server/meta-problems/"+meta_id+"/problems/",
                type: "POST",
                dataType: "json",
                data: {
                    title:$('#title').val(),
                    author:$('#author').val(),
                    source:$('#source').val(),
                    introduction:$('#introduction').val(),
                    status:$('#status').prop("value"),
                    test_type:$('#test_type').prop("value"),
                    description:$('#description').prop("value"),
                    sample:$('#sample').prop("value"),
                },
                success: function (response) {
                    alert('添加成功');
                    location.href='/problem-detail?id='+meta_id;
                },
                error: function (response) {
                    console.log(response);
                }

            });
        });


    });