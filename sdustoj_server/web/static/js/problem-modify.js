/**
 * Created by zzk on 16-8-9.
 */
   $(document).ready(function () {
        var meta_id=$('#meta_id').val();
          $.ajax({
                url: "/api-server/meta-problems/"+meta_id+"/",
                type: "GET",
                dataType: "json",
                data: {
                },
                success: function (response) {
                            $('#title').val(response.title);
                            $('#source').val(response.source);
                    if(response.status==1)
                            $("#status option[value=1]").attr("selected","selected");
                    else
                             $("#status option[value=0]").attr("selected","selected");
                            $('#author').val(response.author);
                            $('#introduction').val(response.introduction);
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
        $('#maketrue').click(function () {
            $.ajax({
                url: "/api-server/meta-problems/"+meta_id+"/",
                type: "PATCH",
                dataType: "json",
                data: {
                    title: $('#title').val(),
                    source: $('#source').val(),
                    status: $('#status').val() == "0" ? 0 : 1,
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