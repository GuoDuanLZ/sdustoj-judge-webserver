/**
 * Created by zzk on 16-8-20.
 */
  $(function () {
        Id = $('#meta_id_hidden').text();
 	    var url="/problem-modify?id="+Id;
        $('#nav_a_modify').attr("href",url);
        $.ajax({
            url: "/api-server/meta-problems/" + Id + "/",
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
                $('#N_description').text(response.number_description);
                $('#N_sample').text(response.number_sample);
                $('#N_test_data').text(response.number_test_data);
                $('#N_problem').text(response.number_problem);

            },
            error: function (response) {

            }

        });
        $('#s_add, #d_add, #t_add').click(function() {
          $('form').find('input').val("");
          $('form').find('textarea').val("");
        });


    });