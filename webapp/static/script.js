$(document).ready(function () {

    $('#startModal').modal('show');
    $('#game-overlay').show();
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
                    $('#game-overlay').hide();
                    $('#message').text('The row is topped out!').show().delay(2000).fadeOut();
                } else if (response.result === 'GAME_OVER_4connected') {
                    // Show who won
                    // const lastMove = [response.y, response.x];
                    // const winningCells = getWinningCells(response.game, lastMove);
                    // if (winningCells) {
                    //     drawWinningLine(winningCells);
                    // }
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
                // Display start modal
                $("#startModal").modal('show');
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
                        // const lastMove = [response.y, response.x];
                        // const winningCells = getWinningCells(response.game, lastMove);
                        // if (winningCells) {
                        //     drawWinningLine(winningCells);
                        // }
                        updateBoard(response.game);
                        var winner = response.coin === 1 ? 'Red' : 'Yellow';
                        $('#message').text(winner + ' wins, shown up by an AI lmao').show();
                        $('#reset-button').show();
                        $('#loading').hide();
                        // $('#game-overlay').hide();
                    } else if (response.result === 'GAME_OVER_nomoremovesleft') {
                        // Show draw message
                        updateBoard(response.game);
                        $('#message').text('The game is a draw!').show();
                        $('#reset-button').show();
                        $('#loading').hide();
                        // $('#game-overlay').hide();
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
        }, 300);  // Delay for 1 seconds
    }



    $('#dark-mode').click(function () {
        $('#body').addClass('darkmode');
        $('#dark-mode').hide();
        $('#light-mode').show();
    });

    $('#light-mode').click(function () {
        $('#body').removeClass('darkmode');
        $('#light-mode').hide();
        $('#dark-mode').show();
    });

    function getWinningCells(board, lastMove) {
        const [row, col] = lastMove;
        const coin = board[row][col];
        const directions = [
            [[-1, 0], [1, 0]], // vertical
            [[0, -1], [0, 1]], // horizontal
            [[-1, -1], [1, 1]], // diagonal from left to right
            [[-1, 1], [1, -1]], // diagonal from right to left
        ];

        for (let [start, end] of directions) {
            const cells = [];

            // Check in the start direction
            let r = row, c = col;
            while (r >= 0 && r < board.length && c >= 0 && c < board[0].length && board[r][c] === coin) {
                cells.push([r, c]);
                r += start[0];
                c += start[1];
            }

            // Check in the end direction
            r = row - start[0], c = col - start[1];
            while (r >= 0 && r < board.length && c >= 0 && c < board[0].length && board[r][c] === coin) {
                cells.push([r, c]);
                r += end[0];
                c += end[1];
            }

            if (cells.length >= 4) {
                // Sort cells by row and column indexes to draw the winning line correctly
                cells.sort((a, b) => (a[0] - b[0]) !== 0 ? (a[0] - b[0]) : (a[1] - b[1]));
                return cells;
            }
        }

        return null;
    }

    function drawWinningLine(cells) {
        var cell = document.querySelector('.game-cell');
        var cellSize = cell.offsetWidth; // Assuming the cell is square
    
        if (cells.length === 0) {
            return;
        }
        
        var canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear previous drawings
        ctx.beginPath();
        ctx.moveTo(cells[0][1] * cellSize + cellSize / 2, cells[0][0] * cellSize + cellSize / 2);
        
    
        for (let i = 1; i < cells.length; i++) {
            ctx.lineTo(cells[i][1] * cellSize + cellSize / 2, cells[i][0] * cellSize + cellSize / 2);
        }
    
        ctx.strokeStyle = 'black'; // Set line color
        ctx.lineWidth = 4; // Set line width
        ctx.stroke();
    }
    


});
