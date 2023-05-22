$(document).ready(function () {

    $('#startModal').modal('show');

    // Handle player choosing to go first
    $('#player-first').click(function () {
        $('#startModal').modal('hide');
        // No need to do anything else, the player will click on the board to make their move
    });

    // Handle player choosing for AI to go first
    $('#ai-first').click(function () {
        $('#startModal').modal('hide');
        takeAiTurn();
    });

    $('#game-overlay').hide();
    $('#game-board').on('click', '.game-cell', function () {
        var x = $(this).data('x');
        
        $('#game-overlay').show();
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
                } else if (response.result === 'next_move') {
                    
                    takeAiTurn();
                    updateBoard(response.game);
                    updatePlayerTurn(response.coin);
                    

                } else {
                    // Update the game board
                    updateBoard(response.game);
                    updatePlayerTurn(response.coin);
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
                $('#game-overlay').hide();
                updateBoard(response.game);
                updatePlayerTurn(response.coin);
                // Hide the reset button and message
                $('#reset-button').hide();
                $('#message').hide();
                // $('#player-turn').hide();
                
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

    function updatePlayerTurn(next_coin) {
        var color = next_coin === 1 ? 'red' : 'yellow';
        $('#player-turn').css('background-color', color).show();
    }
    
    function takeAiTurn() {
        // Show loading animation
        $('#loading').show();
        

        // Delay to simulate AI "thinking"
        setTimeout(function () {
            $.ajax({
                url: '/ai_move',
                type: 'POST',
                success: function (response) {
                    if (response.result === 'GAME_OVER_4connected') {
                        // Show who won
                        updateBoard(response.game);
                        var winner = response.coin === 1 ? 'Red' : 'Yellow';
                        $('#message').text(winner + ' wins, shown up by an AI lmao').show();
                        $('#reset-button').show();
                        $('#loading').hide();
                        $('#game-overlay').hide();
                    } else if (response.result === 'GAME_OVER_nomoremovesleft') {
                        // Show draw message
                        updateBoard(response.game);
                        $('#message').text('The game is a draw!').show();
                        $('#reset-button').show();
                        $('#loading').hide();
                        $('#game-overlay').hide();
                    } else {
                        // Update the game board
                        updateBoard(response.game);
                        updatePlayerTurn(response.coin);
                        $('#loading').hide();
                        $('#game-overlay').hide();
                    }
                    
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }, 700);  // Delay for 1 seconds
    }
    
});
