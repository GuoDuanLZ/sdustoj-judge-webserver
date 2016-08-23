/**
 * Created by zzk on 16-8-22.
 */
$(function(){
    //        测试数据控件
        var test_table = $('#test_data_table').DataTable({
            scrollX: false,
            scrollCollapse: false,
            scrolly: false,
            searching: false,
            paging: false,
            ordering: false,
            ajax: {
                url: "/api-server/problems/" + Id + "/test-data/",
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
                    render: function (data, type, row, meta) {
                        return '<button type="button" id="delete" class="btn btn-outline-danger btn-sm" >删除</button>';
                    }
                }
            ]
        });
        $('#test_modify').click(function () {
            var meta_id = $('#meta_id').text();
            $('#test_Modal').modal('show');
            $.ajax({
                url: "/api-server/meta-problems/" + meta_id + "/test-data/",
                type: "GET",
                dataType: "json",
                data: {},
                success: function (response) {
                    $('#test_select').html('');
                    $.each(response.results, function (i, item) {
                        $('#test_select').append(function () {
                            var op = '<option value="' + item.id + '">' + item.title + '</option>'
                            return op;
                        });
                    });
                },
                error: function (response) {

                    if (response.status == 404) {
                        alert("没找到数据");
                    }
                    else if (response.status == 500) {
                        alert("服务器拥挤");
                    }
                },
            });
        });
        $('#a_test_data').on('shown.bs.tab', function (e) {
            //当切换tab时，强制重新计算列宽
            test_table.columns.adjust().draw();
        });
        $('#t_save').click(function () {
            $.ajax({
                url: "/api-server/problems/" + Id + "/test-data-rel/",
                type: "POST",
                dataType: "json",
                data: {
                    test_data: $('#test_select').prop('value')
                },
                success: function (response) {
                    alert('添加成功');
                    $('#test_Modal').modal('hide');
                    test_table.ajax.reload(null, false);
                },
                error: function (response) {

                    if (response.status == 400) {
                        alert("题目中已存在该测试数据请重新选择");
                    }
                    else if (response.status == 500) {
                        alert("服务器拥挤");
                    }
                },
            });
        });
        test_table.on('click', 'tbody td #delete', function () {
            var t_id = $(this).parent().parent().children().eq(3).text();
            var test_rel_id;
            $.ajax({
                url: "/api-server/problems/" + Id + "/test-data-rel/",
                type: "GET",
                dataType: "json",
                data: {},
                success: function (data) {
                    $.each(data.results, function (i, item) {
                        if (t_id == item.test_data)
                            test_rel_id = item.id;
                    })
                },
                error: function (data) {
                    console.log(data);
                    alert('删除失败');

                }

            });
            if (confirm('是否删除？')) {
                $.ajax({
                    url: "/api-server/problems/" + Id + "/test-data-rel/" + test_rel_id + "/",
                    type: "DELETE",
                    dataType: "json",
                    data: {},
                    success: function (data) {
                        alert('删除成功');
                        test_table.ajax.reload(null, false);

                    },
                    error: function (data) {
                        console.log(data);
                        alert('删除失败');

                    }

                });
            }
        });
})