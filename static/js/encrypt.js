function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]\;',./{}|:<>?~`";
  
    for (var i = 0; i < 30; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    console.log(text)
      $('#key').val(text)
  
  }
  
$('#form').on('submit', function (e) {
    $('#loading').show()
    $('#resultsHeader').html('');
    $('#numberOfWords').html('');
    $('#results').html('');
    let query = $('#textbox').val();
    let key = $('#key').val();
    e.preventDefault();

    let ajaxURL = window.location.href + 'encrypt/'
    $.ajax({
        url: ajaxURL,
        data: { 'text': query,
                 'key': key        
                },
        method: 'POST',
        success: function (data) {
            console.log(data)
            $('#loading').hide();
            $('#keyNote').show();
            let generatedURL = window.location.href + "notes/" + data.generatedID
            $('#noteLink').attr("href", generatedURL);
            $('#yourKey').html("Your key: " + key);
            console.log(window.location.href + "notes/" + data.generatedID)
            //location.href = window.location.href + "notes/" + data;
            
            

        }
    })
})
