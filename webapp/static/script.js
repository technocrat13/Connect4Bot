$(document).ready(function () {
    $('#game-board').on('click', '.game-cell', function () {
        var x = $(this).data('x');
        $.ajax({
            url: '/play',
            data: JSON.stringify({ 'x': x }), // Stringify the data
            contentType: "application/json; charset=utf-8", // Add this line
            type: 'POST',
            success: function (response) {
                if (response.result === 'ERR_rowtoppedout') {
                    // Shake the game board
                    $('#game-board').addClass('shake');
                    setTimeout(function () {
                        $('#game-board').removeClass('shake');
                    }, 500);
                    // Show toast message
                    $('#message').text('The row is topped out!').show().delay(2000).fadeOut();
                } else if (response.result === 'GAME_OVER_4connected') {
                    // Show who won
                    updateBoard(response.game);
                    var winner = response.coin === 1 ? 'Red' : 'Yellow';
                    $('#message').text(winner + ' wins!').show();
                    $('#reset-button').show();
                } else if (response.result === 'GAME_OVER_nomoremovesleft') {
                    // Show draw message
                    updateBoard(response.game);
                    $('#message').text('The game is a draw!').show();
                    $('#reset-button').show();
                } else {
                    // Update the game board
                    updateBoard(response.game);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $('#reset-button').on('click', function () {
        $.ajax({
            url: '/reset',
            type: 'POST',
            contentType: "application/json; charset=utf-8", // Add this line
            success: function (response) {
                // Reset the game board
                updateBoard(response.game);
                // Hide the reset button and message
                $('#reset-button').hide();
                $('#message').hide();
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    function updateBoard(game) {
        $('.game-cell').each(function (index) {
            var value = game[Math.floor(index / 7)][index % 7];
            $(this).data('value', value);
            $(this).attr('data-value', value); 
        });
    }
    
    
});
