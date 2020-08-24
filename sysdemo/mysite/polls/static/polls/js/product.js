    $(function() {
      $('select').addClass('form-control browser-default custom-select custom-select-lg mb-1')
      $('select').attr('style', 'margin-top:-21px;');
      $('select').append('<option value="custom" selected>Select DB</option>');
      
      if ($('#id_active').prop("required")) {
        $("#id_active").prop('required', false);
      }
      
      $('#id_active').bootstrapToggle('on');

      $(':checkbox').change(function() {
        if (!$(this).prop("checked")) {
          $(this).parent().addClass('toggle btn btn-danger btn-primary')

        }
      });
      $("select").change(function() {

        var selectedDatabase = $(this).children("option:selected").val();

        alert("Product Will Be created to - " + selectedDatabase);

        if (selectedDatabase && selectedDatabase != "custom") {
          $("#demo").removeAttr('style');

          $("#data_description").html(`<h1>Current Selection</br>${selectedDatabase}</h1>`);
   
          url = $('#django_form').attr("action") + '/' + selectedDatabase + '/';
     
          $('#django_form').attr("action", url)
        }

      });

      $(".product_close").click(function(ev) { // for each edit contact url

        location.href = "/polls/dashboard/"
        
        return false; // prevent the click propagation
      });

      $(window).bind("pageshow", function(event) {
          if (event.originalEvent.persisted) {
              window.location.reload(); 
          }
      });
    }) 