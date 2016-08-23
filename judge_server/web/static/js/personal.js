/**
 * Created by zzk on 16-8-3.
 */
$(document).ready(function() {
    $('#submit').click(function () {
        $.post({
            url: "/userinfo/",
            data: {
                "firstname": $('#firstname').val(),
                "lastname": $('#lastname').val(),
                "email": $('#email').val()
            },
            success: function (data) {
                if (data == 'true') {
                    alert('修改成功');
                    location.reload()
                }
            }
        });
    });
});