/**
 * Created by zzk on 16-8-9.
 */
$(document).ready(function () {
        $('#maketrue').click(function () {
            $.ajax({
                url: "/api-server/meta-problems/",
                type: "POST",
                dataType: "json",
                data: {
                    title: $('#title').val(),
                     id: $('#id').val(),
                    source: $('#source').val(),
                    status: $('#status').val() == "available" ? 0 : 1,
                    author: $('#author').val(),
                    introduction: $('#introduction').val()
                },
                success: function (data) {
                    alert('成功');
                    location.href = "/problem";
                },
                error: function (response) {
                    console.log(response);
                    if (response.status == 400) {
                        if (response.responseJSON.meta_id[0] == "meta problem with this meta id already exists.") {
                            alert("ID_重复");
                        }
                    }
                }

            });
        });
        $('#cancel').click(function () {
            if (confirm('是否退出修改')) {
                location.href = "/problem";
            }

        });
    });