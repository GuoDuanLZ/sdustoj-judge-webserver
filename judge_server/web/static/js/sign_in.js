$(document).ready(function() {
  $("#form-sign-in").submit(function() {
    var username = $("#input-username").val();
    var password = $("#input-password").val();

    if(username == "" || password == "") {
      $("#h-message").text("用户名或密码不可为空");
      if(username == "") {
        $("#div-username").addClass("has-danger");
      } else {
        $("#div-username").removeClass("has-danger");
      }
      if(password == "") {
        $("#div-password").addClass("has-danger");
      } else {
        $("#div-password").removeClass("has-danger");
      }
      $("#btn-sign-in").addClass("btn-danger").text("登录");
      return false;
    }

    $("#btn-sign-in").removeClass("btn-danger").addClass("btn-info").text("登录中……")

    $.ajax({
      type: "post",
      url: "/api-server/login/",
      dataType: "json",
      data: {
        "username": username,
        "password": password
      },
      success: function(response) {
        $("#btn-sign-in").removeClass("btn-info").addClass("btn-success").text("登录成功")
        //  alert(document.referrer)
         location.href = document.referrer

      },
      error: function(response, info, error) {
        if(response.status == 403) {
          if(response.responseJSON.detail == "Incorrect authentication credentials.") {
            $("#div-username").removeClass("has-danger").addClass("has-danger");
            $("#div-password").removeClass("has-danger").addClass("has-danger");
            $("#h-message").text("用户名或密码错误");
          } else {
            $("#div-username").removeClass("has-danger").addClass("has-danger");
            $("#div-password").removeClass("has-danger").addClass("has-danger");
            $("#h-message").text("该用户已被禁止登录");
          }
        }
        $("#btn-sign-in").removeClass("btn-info").addClass("btn-danger").text("登录");
      }
    });

  });
});
