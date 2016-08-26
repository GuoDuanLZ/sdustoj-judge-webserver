/**
 * Created by zzk on 16-8-20.
 */
$(function () {
          var test_table = $('#test_data_table').DataTable({
            scrollX: false,
            scrollCollapse: false,
            scrolly: false,
            searching: false,
            paging: false,
            ordering: false,
            ajax: {
                url: "/api-server/meta-problems/" + Id + "/test-data/",
                dataSrc: function (result) {
                    result.recordsFiltered = result.count;
                    return result.results;
                },
                data: function (d) {
                }
            },
            columns: [
                {data: "title"},
                {data: "status"},
                {data: "introduction"},
                {data: "id"},
                {data: "meta_problem"},
                {
                    data: "null",
                    width: "150px",
                    render: function (data, type, row, meta) {
                        return '<button id="test_modify" type="button" class="btn btn-outline-primary btn-sm">修改</button> &nbsp; <button type="button" id="delete" class="btn btn-outline-danger btn-sm" >删除</button>';
                    }
                }
            ]
        });
        $('#a_test_data').on('shown.bs.tab', function (e) {
            //当切换tab时，强制重新计算列宽
            test_table.columns.adjust().draw();
        });
    $('#t_add').click(function() {
          $('#t_save').unbind("click");
          $('#t_save').on('click', function() {
            $.ajax({
              url: "/api-server/meta-problems/" + Id + "/test-data/",
              type: "POST",
              dataType: "json",
              data: {
                title: $('#t_title').val(),
                introduction: $('#t_introduction').val(),
                status: $('#t_status').val() == "1" ? 1 : 0,
                test_in: $('#test_in').val(),
                test_out: $('#test_out').val(),
              },
              success: function (response) {
                  alert('添加成功');
                  $('#test_Modal').modal('hide');
                  test_table.ajax.reload(null, false);
              },
              error: function (response) {
                if(response.status==400){
                  alert("标题不能为空");
                }
                else if(response.status==404){
                  alert("没有找到资源");
                }
                else if(response.status==500){
                  alert("服务器拥挤");
                }

              },
            });
          });
        });
         test_table.on('click', 'tbody td #test_modify', function() {
          var t_id=$(this).parent().parent().children().eq(3).text();
          $.ajax({
            url: "/api-server/meta-problems/" + Id + "/test-data/"+ t_id +"/",
            type: "GET",
            dataType: "json",
            data:{

            },
            success: function(response) {
            $('#t_title').val(response.title);
            $('#t_introduction').val(response.introduction);
            $('#t_id').val(response.id);
            if(response.status==1)
            {
               $("#t_status option[value=1]").prop("selected","selected");
            }
            else{
              $("#t_status option[value=0]").prop("selected","selected");
            }
            $('#test_in').val(response.test_in);
            $('#test_out').val(response.test_out);
            },
            error: function(response) {
              console.log(response);
                if(response.status==404){
                  alert("没有找到资源");
                }
                else if(response.status==500){
                  alert("服务器拥挤");
                }
            },
          });
          $('#t_save').unbind("click");
              $('#t_save').on('click', function() {
                $.ajax({
                    url: "/api-server/meta-problems/" + Id + "/test-data/"+ t_id +"/",
                    type: "PATCH",
                    dataType: "json",
                    data: {
                         title: $('#t_title').val(),
                         introduction: $('#t_introduction').val(),
                         status: $('#t_status').val() == "1" ? 1 : 0,
                         test_in: $('#test_in').val(),
                         test_out: $('#test_out').val(),

                    },
                    success: function (response) {
                        alert('修改成功');
                       // location.reload(true);
                        $('#test_Modal').modal('hide');
                        test_table.ajax.reload(null, false);
                    },
                    error: function (response) {
                    if(response.status==400){
                      alert("标题不能为空");
                    }
                    else if(response.status==404){
                      alert("没有找到资源");
                    }
                    else if(response.status==500){
                      alert("服务器拥挤");
                    }

                    },
                });
              });
          $('#test_Modal').modal('show');
        });
    test_table.on('click', 'tbody td #delete', function () {
        var t_id = $(this).parent().parent().children().eq(3).text();
        if (confirm('是否删除？')) {
            $.ajax({
                url: "/api-server/meta-problems/" + Id + "/test-data/" + t_id + "/",
                type: "DELETE",
                dataType: "json",
                data: {},
                success: function (data) {
                    test_table.ajax.reload(null, false);

                },
                error: function (data) {
                    console.log(data);
                    alert('删除失败');

                }

            });
        }
    });
     // 测试数据输入更新文件上传
     $('#t_in_submit').click(function() {
          var in_id=$('#t_in_ID').val();
         $.ajax({
                url: '/api-server/meta-problems/'+Id+'/test-data-in/'+in_id+'/',
                type: 'PATCH',
                cache: false,
                data: new FormData($('#test_in_form')[0]),
                processData: false,
                contentType: false,
                success:function(){
                     alert('修改成功');
                     $('#test_file_in_Modal').modal('hide');
                        test_table.ajax.reload(null, false);
                }
                })
     });
      // 测试数据输出更新文件上传
    $('#t_out_submit').click(function(){
        var out_id= $('#t_out_ID').val()
         $.ajax({
                url: '/api-server/meta-problems/'+Id+'/test-data-out/'+out_id+'/',
                type: 'PATCH',
                cache: false,
                data: new FormData($('#test_out_form')[0]),
                processData: false,
                contentType: false,
                success:function(){
                     alert('修改成功');
                     $('#test_file_out_Modal').modal('hide');
                        test_table.ajax.reload(null, false);
                }
         })
    });
     $('#t_file_in_download').click(function(){
        var in_id= $('#ID_test').val()
         window.open('/api-server/meta-problems/'+Id+'/test-data-files/'+in_id+'/in/');
    });
     $('#t_file_out_download').click(function(){
        var out_id= $('#ID_test').val()
          window.open('/api-server/meta-problems/'+Id+'/test-data-files/'+out_id+'/out/');
    });

    $('#t_file_save').click(function(){
         $.ajax({
                url: '/api-server/meta-problems/'+Id+'/test-data-files/',
                type: 'POST',
                cache: false,
                data: new FormData($('#test-file-from')[0]),
                processData: false,
                contentType: false,
                success:function(){
                     alert('添加成功');
                       // location.reload(true);

                        $('#test_file_Modal').modal('hide');
                        test_table.ajax.reload(null, false);
                }})
    });


});