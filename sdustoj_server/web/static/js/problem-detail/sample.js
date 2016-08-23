/**
 * Created by zzk on 16-8-20.
 */
$(function () {
        var sam_table = $('#sample_table').DataTable({
            scrollX: false,
            scrollCollapse: false,
            scrolly: false,
            searching: false,
            paging: false,
            ordering: false,
            ajax: {
                url: "/api-server/meta-problems/" + Id + "/samples/",
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
                        return '<button id="sim_modify" type="button" class="btn btn-outline-primary btn-sm">修改</button> &nbsp; <button type="button" id="delete" class="btn btn-outline-danger btn-sm" >删除</button>';
                    }
                },

            ]
        });
        $('#a_sample').on('shown.bs.tab', function (e) {
            //当切换tab时，强制重新计算列宽
            sam_table.columns.adjust().draw();
        });
     $('#s_add').click(function() {
          $('#s_save').unbind("click");
          $('#s_save').on('click', function() {
              $.ajax({
                  url: "/api-server/meta-problems/" + Id + "/samples/",
                  type: "POST",
                  dataType: "json",
                  data: {
                       title: $('#s_title').val(),
                       introduction: $('#s_introduction').val(),
                       status: $('#s_status').val() == "1" ? 1 : 0,
                       content: $('#s_content').val(),

                  },
                  success: function (response) {
                      alert('添加成功');
                       $('#sam_Modal').modal('hide');
                        sam_table.ajax.reload(null, false);
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

        sam_table.on('click', 'tbody td #sim_modify', function() {
          var s_id=$(this).parent().parent().children().eq(3).text();
          $.ajax({
            url: "/api-server/meta-problems/" + Id + "/samples/"+ s_id +"/",
            type: "GET",
            dataType: "json",
            data:{

            },
            success: function(response) {
            $('#s_title').val(response.title);
            $('#s_introduction').val(response.introduction);
            $('#s_id').val(response.id);
            if(response.status==1)
            {
               $("#s_status option[value=1]").prop("selected","selected");
            }
            else{
              $("#s_status option[value=0]").prop("selected","selected");
            }
            $('#s_content').val(response.content);
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
          $('#s_save').unbind("click");
              $('#s_save').on('click', function() {
                $.ajax({
                    url: "/api-server/meta-problems/" + Id + "/samples/"+ s_id +"/",
                    type: "PATCH",
                    dataType: "json",
                    data: {
                         title: $('#s_title').val(),
                         introduction: $('#s_introduction').val(),
                         status: $('#s_status').val() == "1" ? 1 : 0,
                         content: $('#s_content').val(),

                    },
                    success: function (response) {
                        alert('修改成功');
                         $('#sam_Modal').modal('hide');
                        sam_table.ajax.reload(null, false);
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
          $('#sam_Modal').modal('show');
        });
        sam_table.on('click','tbody td #delete',function(){
          var s_id=$(this).parent().parent().children().eq(3).text();
                 if(confirm('是否删除？'))
           {
                 $.ajax({
              url:"/api-server/meta-problems/" + Id + "/samples/" + s_id +"/",
              type:"DELETE",
              dataType:"json",
              data:{
              },
              success:function (data) {
                   sam_table.ajax.reload(null, false);

              },
              error:function (data) {
                   console.log(data);
                   alert('删除失败');

              }

                 });
           }
          });
});