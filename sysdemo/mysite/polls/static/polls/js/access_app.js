$(function() {
  var $list = $("#django_form :input[type='text']");
  $list.each(function() {
    $(this).attr('placeholder', $(this).attr('label'))
    $(this).addClass('form-control')
  });

  var $list = $("#id_description");
  $list.each(function() {
    $(this).parent().addClass('col-sm-12')
    $(this).attr('placeholder', $(this).attr('label'))
    $(this).addClass('form-control')
  });

  var $list = $("#id_address");
  $list.each(function() {
    $(this).attr('placeholder', $(this).attr('name'))
    $(this).addClass('form-control')
  });

  var $list = $("#id_age");
  $list.each(function() {
    $(this).attr('placeholder', $(this).attr('name'))
    $(this).addClass('form-control')
  });

  var $list = $("#django_form :input[id='id_username']");
  $list.each(function() {
    $(this).attr('placeholder', $(this).attr('name'))
    $(this).addClass('form-control')
  });

  var $list = $("#id_password");
  $list.each(function() {
    $(this).attr('placeholder', $(this).attr('name'))
    $(this).addClass('form-control')
  });

  var $list = $("#id_password1");
  $list.each(function() {
    $(this).attr('placeholder', "password")
    $(this).addClass('form-control')
  });

  var $list = $("#id_email");
  $list.each(function() {
    $(this).attr('placeholder', $(this).attr('name'))
    $(this).addClass('form-control')
  });

  var $list = $("#id_password2");
  $list.each(function() {
    $(this).attr('placeholder', "confirm_password")
    $(this).addClass('form-control')
  });

  var $list = $("#django_form :input[type='number']");
  $list.each(function() {
    $(this).attr('placeholder', $(this).attr('label'))
    $(this).addClass('form-control')
  });

  $("#django_form").submit(function(event) {
    if ($("input[id='id_username']").val().length < 8) {
      $("input[type='text']").next().text("user name less than 8 Character").show();
      event.preventDefault();
      return;
    }
    if ($("input[type='password']").val().length < 8) {
      $("input[type='password']").next().text("password less than 8 Character").show();
      event.preventDefault();

      return;
    }

  });

  $('#id_database_access li').addClass("list-group checked-list-box")
  $('#id_database_access').css("padding-left", 0)
  $('#id_database_access li label').css("color", "black")


  $('#product_create_modal').modal({
    backdrop: 'static',
    keyboard: false
  })

  $('#product_create_modal').modal({
    backdrop: 'static',
    keyboard: false
  })
  $('.save_value').click(function() {
    var db_array = ['database_1', 'database_2', 'database_3', 'database_4', 'database_5']
    var array = [];
    var profile_id = null
    var csrfToken = null
    $(this).closest('td').siblings().find('input[type=checkbox]').each(function(i) {
      profile_id = $(this).attr("id")
      if ($(this).is(":checked")) {
        array.push(db_array[i])
      }
    });

    $.ajax({
      url: '/polls/edit_permission/' + profile_id + "/",
      type: 'put', // This is the default though, you don't actually need to always mention it
      dataType: 'json',
      data: {
        database_access: array
      },
      headers: {
        "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').val()
      },

      success: function(data) {
        location.reload(true)

      },
      failure: function(data) {
        alert('Error Occured');
      }
    });

  });

  $(".li-modal").click(function(ev) {
    ev.preventDefault();
    var target = $(this).attr("href");

    // load the url and show modal on success
    $("#signupModel .modal-content").load(target, function() {
      $('#signupModel').modal({
        backdrop: 'static',
        keyboard: false
      })
      $("#signupModel").modal("show");

    });
    return false
  });

  $(".model_loder").click(function(ev) {
    ev.preventDefault();
    location.reload(true)
    return false
  })

  $("#profile_alert").click(function() {

    var selectedDatabase = $(this).children("option:selected").val();

    alert("Profile functionality is not implemented yet");
  })

  if (window.location.pathname == '/polls/signup/') {
    $('#signupModel').modal('hide')
    $('#signupload').modal('show').find('.modal-content').html($('#form_model_id').html());
    $('#form_model_id').empty()
    return false
  }

  if (window.location.pathname == '/polls/product' || window.location.pathname == '/polls/product/') {

    $('#signupload').modal('hide')
    var data = $('#product_model_id').html()
    $('#product_model_id').empty()
    $('#product_create_modal').modal('show').find('.modal-content').html(data);
    return false
  }


  $(".data-dismiss").click(function(ev) { // for each edit contact url
    ev.preventDefault(); // prevent navigation
    return false; // prevent the click propagation
  });


  $('#id_database_access li').each(function(i) {

    $(this).addClass("list-group-item")

  });
  setTimeout(function() {
    if ($('#msg').length > 0) {
      $('#msg').remove();
    }
  }, 2000)

  $(window).bind("pageshow", function(event) {
    if (event.originalEvent.persisted) {
      window.location.reload();
    }
  });
})