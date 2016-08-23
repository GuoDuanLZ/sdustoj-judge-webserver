/**
 * Created by zzk on 16-8-20.
 */
$(function () {
    var pro_table = $('#problem_table').DataTable({
        scrollX: false,
        scrollCollapse: false,
        scrolly: false,
        searching: false,
        paging: false,
        ordering: false,
        ajax: {
            url: "/api-server/meta-problems/" + Id + "/problems/",
            dataSrc: function (result) {
                result.recordsFiltered = result.count;
                return result.results;
            },
            data: function (d) {
            }
        },
        columns: [
            {
                data: "title",
                render: function (data, type, row, meta) {
                    return "<a href='/pro-detail?id=" + row.id + "'>" + data + "</a>"
                }
            },
            {data: "status",
                width: "50px",
            render:function(data, type, row, meta) {
                return "<div style='text-align:right;'>"+data+"</div>";
            }},
            {data: "introduction"},
            {data: "id",
            width: "50px",
              render:function(data, type, row, meta) {
                return "<div style='text-align:right;'>"+data+"</div>";
            }},
            {data: "source",
            width: "100px",},
            {data: "author",
            width: "100px",},
            {
                data: "null",
                width: "150px",
                render: function (data, type, row, meta) {
                    return '<button type="button" id="modify" class="btn btn-outline-info btn-sm" >修改</button>&nbsp;&nbsp;<button type="button" id="delete" class="btn btn-outline-danger btn-sm" >删除</button>';
                }
            },
        ]
    });
    $('#a_problem').on('shown.bs.tab', function (e) {
        //当切换tab时，强制重新计算列宽
        pro_table.columns.adjust().draw();
    });
    pro_table.on('click', 'tbody td #delete', function () {
        var pro_id = $(this).parent().parent().children().eq(3).text();
        if (confirm('是否删除？')) {
            $.ajax({
                url: "/api-server/meta-problems/" + Id + "/problems/" + pro_id + "/",
                type: "DELETE",
                dataType: "json",
                data: {},
                success: function (data) {
                    pro_table.ajax.reload(null, false);
                },
                error: function (data) {
                    console.log(data);
                }

            });
        }

    });
    pro_table.on('click', 'tbody td #modify', function () {
        var pro_id = $(this).parent().parent().children().eq(3).text();
        location.href='/pro-modify?problem_id='+pro_id+'&meta_id='+Id;

    });

});