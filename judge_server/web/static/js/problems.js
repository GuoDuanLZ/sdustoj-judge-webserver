$(function(){
    $('#order1').click(function () {
                if (tableorder == 'title')
                    tableorder = '-title';
                else
                    tableorder = 'title';
            });
            $('#order2').click(function () {
                if (tableorder == 'id')
                    tableorder = '-id';
                else
                    tableorder = 'id';
            });
             $('#order7').click(function () {
                if (tableorder == 'create_time')
                    tableorder = '-create_time';
                else
                    tableorder = 'create_time';
            });
            $('#order8').click(function () {
                if (tableorder == 'update_time')
                    tableorder = '-update_time';
                else
                    tableorder = 'update_time';
            });

            var table = $('#example').DataTable({
                columnDefs: [
                    {"orderable": false, "targets": 2},
                    {"orderable": false, "targets": 3},
                    {"orderable": false, "targets": 4},
                    {"orderable": false, "targets": 5},
                ],
                ajax: {
                    url: '/api-server/problems/',
                    dataSrc: function (result) {
                        result.recordsFiltered = result.count;
                        return result.results;
                    },
                    data: function (d) {
                        d.offset = tablestart;
                        d.limit = tablelength;
                        d.search = tablesearch;
                        d.ordering = tableorder;
                    }
                },
                columns: [
                    {data: "title",
                    render:function (data, type, row, meta) {
                        return "<a href='/pro-detail?id="+row.id+"'>"+data+"</a>"
                    }},
                    {data: "id"},
                    {data: "status"},
                    {data: "introduction"},
                    {data: "test_type"},
                    {data: "meta_problem"},
                    {data: "create_time",
                    render:function(data,type,row,meta){
                        var time=data.replace('T',' ');
                        time=time.substring(0,19);
                        return '<center>'+time+'</center>';
                    }},
                    {data: "update_time",
                      render:function(data,type,row,meta){
                        var time=data.replace('T',' ');
                        time=time.substring(0,19);
                        return '<center>'+time+'</center>';
                    }},
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
           });