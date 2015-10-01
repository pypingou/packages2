package_history = function(package) {
  console.log(package);
  var _url = '/api/history/' + package;
  $.ajax({
      url: _url,
      type: 'GET',
      dataType: 'json',
      success: function(res) {
        console.log(res);
        $('#history-cards').html(res.text);
      },
  });

  return false;
}
