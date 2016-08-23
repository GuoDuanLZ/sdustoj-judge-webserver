/**
 * Created by zzk on 16-8-22.
 */
    $(function () {
        Id = $('#id_hidden').text();
//        详情控件
        $.ajax({
            url: "/api-server/problems/" + Id + "/",
            type: "GET",
            dataType: "json",
            data: {},
            success: function (response) {
                $('#title').text(response.title);
                $('#id').text(response.id);
                $('#source').text(response.source);
                $('#author').text(response.author);
                $('#introduction').text(response.introduction);
                $('#status').text(response.status);
                $('#meta_id').text(response.meta_problem);
            },
            error: function (response) {
                if (response.status == 500) {
                    alert("服务器拥挤");
                }
            }

        });

//        描述控件
        $('#a_description').on('click', function () {
            $('#des_panerl,#sam_panerl').text('');
            $.ajax({
                url: "/api-server/problems/" + Id + "/description/",
                type: "GET",
                dataType: "json",
                data: {},
                success: function (response) {
                    $('#des_panerl').text(response.content);
                },
                error: function (response) {

                    if (response.status == 404) {
                        alert("没有找到资源");
                    }
                    else if (response.status == 500) {
                        alert("服务器拥挤");
                    }

                },
            });
            $.ajax({
                url: "/api-server/problems/" + Id + "/sample/",
                type: "GET",
                dataType: "json",
                data: {},
                success: function (response) {
                    $('#sam_panerl').text(response.content);
                },
                error: function (response) {

                    if (response.status == 404) {
                        alert("没有找到资源");
                    }
                    else if (response.status == 500) {
                        alert("服务器拥挤");
                    }
                },
            });
        });
    });