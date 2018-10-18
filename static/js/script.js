$('#form').on('submit', function (e) {
    $('#loading').show()
    $('#resultsHeader').html('');
    $('#numberOfWords').html('');
    $('#results').html('');
    var query = $('#search').val();
    e.preventDefault();

    let ajaxURL = window.location.href + 'scrabble/'
    $.ajax({
        url: ajaxURL,
        data: { 'letters': query },
        method: 'POST',
        success: function (data) {
            $('#search').val('');
            $('#resultsHeader').html('Possible words for ' + query.toUpperCase() + ': <br>')
            handleData(data);
        }
    })
})

String.prototype.replaceAll = function (search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function handleData(data) {
    console.log(data)
    // Convert string returned by python into a JS array
    data = data.replaceAll('\\[', '');
    data = data.replaceAll('\\]', '');
    data = data.replaceAll('\\"', '');
    data = data.replaceAll(' ', '');
    data = data.split(',');

    // Display number of words found
    numberOfWords = data.length
    console.log("Number of found words: " + numberOfWords)
    $('#numberOfWords').html('<strong>' + numberOfWords + ' found!' + '<strong')

    // Find max length of words found
    let maxLength = 0
    data.forEach(function (word) {
        if (word.length > maxLength) {
            maxLength = word.length;
        }
    });
    console.log("Max word length is: " + maxLength)

    // create 2 Dimensional array to hold words, based on length
    // There is an array for each length of word, from 0 to maxLength
    // 2 letter words, 3 letter words, etc.
    var allArrays = new Array(maxLength);
    for (i = 0; i < maxLength + 1; i++) {
        allArrays[i] = new Array();
        data.forEach(function (word) {
            if (word.length == i) {
                allArrays[i].push(word);
            }
        });
    };
    console.log(allArrays);

    // find which arrays have words in them and append them to #results
    let counter = 0
    allArrays.forEach(function (array) {
        console.log(counter + " letter words:");
        console.log(array);
        var currentResults = $('#results' + counter);
        console.log(currentResults);
        console.log('above');
        if (array.length != 0) {
            if(currentResults.length < 1){
                // window['divResults' + counter]
                var itemResults = document.createElement('div');
                itemResults.id = 'flex-item--results' + counter;
                document.body.appendChild(itemResults);
                console.log('below');
                console.log(itemResults);
            }
            $(itemResults).append('<div class="flex-item--header">'+ counter + ' letter words: <br> </div>');
            for(i in array){
                $(itemResults).append('<li>' +  array[i]  + '</li>');
                console.log(array[i]);
            }
            $('#flex-row').append($(itemResults));
        }
        counter++;
    });
    $('#loading').hide()
}