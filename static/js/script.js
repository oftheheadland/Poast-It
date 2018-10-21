



$('#form').on('submit', function (e) {
    $('#loading').show()
    $('#resultsHeader').html('');
    $('#numberOfWords').html('');
    $('#results').html('');
    var query = $('#textbox').val();
    e.preventDefault();

    let ajaxURL = window.location.href + 'post/'
    $.ajax({
        url: ajaxURL,
        data: { 'text': query },
        method: 'POST',
        success: function (data) {
            console.log(data)
            $('#loading').hide()
            console.log(window.location.href + "notes/" + data)
            location.href = window.location.href + "notes/" + data;
            
            

        }
    })
})
