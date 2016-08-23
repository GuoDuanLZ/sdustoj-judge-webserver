/**
 * Created by zzk on 16-8-20.
 */
$(function(){
            var des_table = $('#des_table').DataTable({
            scrollX: false,
            scrollCollapse: false,
            scrolly: false,
            searching: false,
            paging: false,
            ordering: false,
            ajax: {
                url: "/api-server/meta-problems/" + Id + "/descriptions/",
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
                        return '<button id="des_modify" type="button" class="btn btn-outline-primary btn-sm">修改</button> &nbsp; <button type="button" id="delete" class="btn btn-outline-danger btn-sm" >删除</button>';
                    }
                }
            ]
        });
        $('#a_description').on('shown.bs.tab', function (e) {
            //当切换tab时，强制重新计算列宽
            des_table.columns.adjust().draw();
        });
        $('#d_add').click(function() {
          $('#d_save').unbind("click");
          $('#d_save').on('click', function() {
            $.ajax({
              url: "/api-server/meta-problems/" + Id + "/descriptions/",
              type: "POST",
              dataType: "json",
              data: {
                title: $('#d_title').val(),
                introduction: $('#d_introduction').val(),
                status: $('#d_status').val() == "1" ? 1 : 0,
                content: $('#d_content').val(),
              },
              success: function (response) {
                  alert('添加成功');
                  $('#des_Modal').modal('hide');
                        des_table.ajax.reload(null, false);
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
        des_table.on('click','tbody td #des_modify', function() {
          var d_id=$(this).parent().parent().children().eq(3).text();
          $.ajax({
            url: "/api-server/meta-problems/" + Id + "/descriptions/"+ d_id +"/",
            type: "GET",
            dataType: "json",
            data:{

            },
            success: function(response) {
            $('#d_title').val(response.title);
            $('#d_introduction').val(response.introduction);
            $('#d_id').val(response.id);
            if(response.status==1)
            {
               $("#d_status option[value=1]").prop("selected","selected");
            }
            else{
              $("#d_status option[value=0]").prop("selected","selected");
            }
            $('#d_content').val(response.content);
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
          $('#d_save').unbind("click");
              $('#d_save').on('click', function() {
                $.ajax({
                    url: "/api-server/meta-problems/" + Id + "/descriptions/"+ d_id +"/",
                    type: "PATCH",
                    dataType: "json",
                    data: {
                         title: $('#d_title').val(),
                         introduction: $('#d_introduction').val(),
                         status: $('#d_status').val() == "1" ? 1 : 0,
                         content: $('#d_content').val(),

                    },
                    success: function (response) {
                        alert('修改成功');
                         $('#des_Modal').modal('hide');
                        des_table.ajax.reload(null, false);
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
          $('#des_Modal').modal('show');
        });
        des_table.on('click','tbody td #delete',function(){
          var d_id=$(this).parent().parent().children().eq(3).text();
                 if(confirm('是否删除？'))
           {
                 $.ajax({
              url:"/api-server/meta-problems/" + Id + "/descriptions/" + d_id +"/",
              type:"DELETE",
              dataType:"json",
              data:{
              },
              success:function (data) {
                   des_table.ajax.reload(null, false);

              },
              error:function (data) {
                   console.log(data);
                   alert('删除失败');

              }

                 });
           }
            });
});