/**
 * Created by zzk on 16-8-3.
 */
$(document).ready(function() {
    $(function () {
        $('#submit').click(function () {
            $.post("/passwordSET/", {
                'username': $('#username').val(),
                'oldpassword': $('#oldpwd').val(),
                'newpassword': $('#newpwd').val()
            }, function (data) {
                if (data == 'true') {
                    alert('修改成功');
                    location.reload()

                }
                else if (data == 'false') {
                    alert('旧密码输入错误，修改失败');
                    location.reload();
                }
            });
        });
        $('#renewpwd').blur(function () {
            var pwd = $('#newpwd').val();
            var repwd = $('#renewpwd').val();
            if (pwd != repwd)
                alert('两次输入密码不匹配');
        });
    });
});