$('#decrypt').on('submit', function (e) {
    $('#loading').show()
    $('#resultsHeader').html('');
    $('#numberOfWords').html('');
    $('#results').html('');
    let query = $('#textbox').val();
    let key = $('#key').val();
    e.preventDefault();

    let ajaxURL = 'http://127.0.0.1:5000/decrypt/'
    $.ajax({
        url: ajaxURL,
        data: { 'text': query,
                'key': key },
        method: 'POST',
        success: function (data) {
            console.log(data)
            $('#loading').hide()
            if (data.decrypted == '' || data == 'failed') {
                $('#decrypted').html('Incorrect key.') 
            }
            else {
                $('#decrypted').html(data.decrypted)
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
        $('#loading').hide()
        $('#decrypted').html("Error") 
    }
    })
})
