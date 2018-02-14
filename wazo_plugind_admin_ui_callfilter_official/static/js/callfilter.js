$(document).ready(function () {
  $('#caller_id_mode').on('change', function (e) {
    toggle_callerid_mode.call(this)
  })
  toggle_callerid_mode.call($('#caller_id_mode'))
});


function toggle_callerid_mode() {
  if ($(this).val() == '') {
    $('#caller_id_name').closest('div.form-group').hide()
  } else {
    $('#caller_id_name').closest('div.form-group').show()
  }
}