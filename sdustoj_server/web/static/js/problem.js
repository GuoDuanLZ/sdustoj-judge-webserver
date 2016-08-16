/**
 * Created by zzk on 16-8-9.
 */
 $(function () {
            $('#order2').click(function () {
                if (tableorder == 'id')
                    tableorder = '-id';
                else
                    tableorder = 'id';
            });
            var table = $('#example').DataTable({
                columnDefs: [
                    {"orderable": false, "targets": 0},
                    {"orderable": false, "targets": 2},
                    {"orderable": false, "targets": 3},
                    {"orderable": false, "targets": 4},
                    {"orderable": false, "targets": 5},
                    {"orderable": false, "targets": 6}
                ],
                ajax: {
                    url: '/api-server/meta-problems/',
                    dataSrc: function (result) {
                        result.recordsFiltered = result.count;
                        return result.results;
                    },
                    data: function (d) {
                        sessionStorage.search = tablesearch;
                        sessionStorage.ordering = tableorder;
                        sessionStorage.limit = tablelength;
                        sessionStorage.start = tablestart;
                        d.offset = tablestart;
                        d.limit = tablelength;
                        d.search = tablesearch;
                        d.ordering = tableorder;
                    }
                },
                columns: [
                    {data: "title",
                    render:function (data, type, row, meta) {
                        return "<a href='/problem-detail?id="+row.id+"'>"+data+"</a>"
                    }},
                    {data: "id"},
                    {data: "source"},
                    {data: "author"},
                    {data: "status"},
                    {data: "introduction"},
                    {
                        data: null,
                        width: "150px",
                        render: function (data, type, row, meta) {
                            return '<button id="modify" type="button" class="btn btn-outline-primary btn-sm">修改</button> &nbsp; <button type="button" id="delete" class="btn btn-outline-danger btn-sm" >删除</button>';
                        }
                    }
                ]
            });

            table.on('length.dt', function (e, settings, len) {
                tablelength = len;
            });
            table.on('page.dt', function (e, settings) {
                tablestart = (table.page()) * tablelength;
            });
            table.on('search.dt', function () {
                tablesearch = table.search();
                tablestart = 0;
            });
           table.on('click','tbody td #delete',function(){
                var meta_id=$(this).parent().parent().children().eq(1).text();
                 if(confirm('是否删除？'))
           {
                 $.ajax({
              url:"/api-server/meta-problems/"+meta_id+"/",
              type:"DELETE",
              dataType:"json",
              data:{
              },
              success:function (data) {
                   table.ajax.reload(null, false);
              },
              error:function (data) {
                   console.log(data);
              }

                 });
           }
            });
             table.on('click','tbody td #modify',function(){
                  var meta_id=$(this).parent().parent().children().eq(1).text();
                 location.href='/problem-modify?meta_id='+meta_id;
             })
           });