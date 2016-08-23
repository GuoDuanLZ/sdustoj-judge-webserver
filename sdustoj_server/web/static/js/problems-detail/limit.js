/**
 * Created by zzk on 16-8-22.
 */
$(function(){
    //        限制控件
        var limit_table = $('#limit_table').DataTable({
            scrollX: false,
            scrollCollapse: false,
            scrolly: false,
            searching: false,
            paging: false,
            ordering: false,
            ajax: {
                url: "/api-server/problems/" + Id + "/limits/",
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
                {data: "environment"},
                {data: "time_limit"},
                {data: "memory_limit"},
                {data: "length_limit"},
                {
                    data: "null",
                    render: function (data, type, row, meta) {
                        return '<button type="button" id="modify"  name="limits" class="btn btn-outline-info btn-sm">修改</button>&nbsp;&nbsp;<button type="button" id="delete" class="btn btn-outline-danger btn-sm" >删除</button>';
                    }
                }
            ]
        });

        $('#a_limit').on('shown.bs.tab', function (e) {
            //当切换tab时，强制重新计算列宽
            limit_table.columns.adjust().draw();
        });

        $('button[name="limits"]').click(function () {
            $('#limit_Modal').modal('show');
            $.ajax({
                url: "/api-server/environments/",
                data: {},
                type: "GET",
                dataType: "json",
                success: function (data) {
                    $('#environment_limit').html('');
                    $.each(data.results, function (i, item) {
                        $('#environment_limit').append(function () {
                            var op = '<option value="' + item.eid + '">' + item.language + '</option>'
                            return op;
                        });
                    });
                },
                error: function (data) {
                    if (response.status == 404) {
                        alert("没有请求到数据");
                    }
                    else if (response.status == 500) {
                        alert("服务器拥挤");
                    }
                }
            });
        });

        limit_table.on('click', 'table td #modify', function () {
            var limit_id=$(this).parent().parent().children().eq(3);
            $.ajax({
                url: "/api-server/problems/" + Id + "/limits/"+limit_id+"/",
                data: {},
                type: "GET",
                dataType: "json",
                success: function (data) {
                            $('#l_title').val(data.tatil);
                            $('#l_introduction').val(data.introduction);
                            $('#l_status').each(function(i,item){
                                var op=$(this).val();
                                if(op==item.status)
                                    $(this).prop('selected','selected');
                            });
                            $('#environment_limit').each(function(i,item){
                                var op=$(this).val();
                                if(op==item.environment)
                                    $(this).prop('selected','selected');
                            });
                            $('#time_limit').val(data.time_limit);
                            $('#memory_limit').val(data.memory_limit);
                            $('#length_limit').val(data.length_limit);
                },
                error: function () {
                         if (response.status == 404) {
                        alert("没有请求到数据");
                    }
                    else if (response.status == 500) {
                        alert("服务器拥挤");
                    }
                },

            });
            $('#l_save').unbind('click');
            $('#l_sava').click(function () {
                $.ajax({
                    url: "/api-server/problems/" + Id + "/limits/",
                    data: {
                        title: $('#l_title').val(),
                        introduction: $('#l_introduction').val(),
                        status: $('#l_status').prop("value"),
                        environment: $('#environment_limit').prop("value"),
                        time_limit: $('#time_limit').val(),
                        memory_limit: $('#memory_limit').val(),
                        length_limit: $('#length_limit').val(),
                    },
                    type: "PATCH",
                    dataType: "json",
                    success: function () {
                        alert('修改成功');
                        $('#limit_Modal').modal('hide');
                        limit_table.ajax.reload(null, false);
                    },
                    error: function () {
                         if (response.status == 404) {
                            alert("没有请求到数据");
                    }
                        else if (response.status == 500) {
                            alert("服务器拥挤");
                    }
                     else if(response.status==400){
                            alert("测试环境不能为空")
                         }
                    },
                })
            });
        });

        $('#limit_add').click(function(){
            $('#l_save').unbind('click');
            $('#l_sava').click(function () {
                $.ajax({
                    url: "/api-server/problems/" + Id + "/limits/",
                    data: {
                        title: $('#l_title').val(),
                        introduction: $('#l_introduction').val(),
                        status: $('#l_status').prop("value"),
                        environment: $('#environment_limit').prop("value"),
                        time_limit: $('#time_limit').val(),
                        memory_limit: $('#memory_limit').val(),
                        length_limit: $('#length_limit').val(),
                    },
                    type: "POST",
                    dataType: "json",
                    success: function () {
                        alert('添加成功');
                        $('#limit_Modal').modal('hide');
                        limit_table.ajax.reload(null, false);
                    },
                    error: function () {
                         if (response.status == 404) {
                            alert("没有请求到数据");
                    }
                        else if (response.status == 500) {
                            alert("服务器拥挤");
                    }
                        else if(response.status==400){
                            alert("测试环境不能为空")
                         }
                    },
                })
            });
        });

        limit_table.on('click','table td #delete',function(){
             var limit_id=$(this).parent().parent().children().eq(3);
            if (confirm('是否删除？')) {
                $.ajax({
                    url: "/api-server/problems/" + Id + "/limit/" + limit_id + "/",
                    type: "DELETE",
                    dataType: "json",
                    data: {},
                    success: function (data) {
                        alert('删除成功');
                        limit_table.ajax.reload(null, false);

                    },
                    error: function (data) {
                        console.log(data);
                        alert('删除失败');

                    }

                });
            }
        });
})
