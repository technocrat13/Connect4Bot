// document.querySelectorAll('.cell').forEach(cell => {
//     cell.addEventListener('click', event => {
//         // Get the coordinates of the clicked cell
//         const col = event.target.getAttribute('data-col');

//         // Make a move
//         fetch('/move', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({x_pos: col})
//         })
//         .then(response => response.json())
//         .then(data => {
//             // Update the game state
//             gameState = data.gameboard;
//             isGameEnded = data.is_game_ended;

//             // Update the UI
//             updateUI();
//         });
//     });
// });

// let gameState = [];
// let isGameEnded = false;

// function updateUI() {
//     // Update the colors of the cells based on the current game state
//     document.querySelectorAll('.cell').forEach(cell => {
//         const row = cell.getAttribute('data-row');
//         const col = cell.getAttribute('data-col');
//         const player = gameState[row][col];
//         if (player == 1) {
//             cell.classList.add('red');
//         } else if (player == -1) {
//             cell.classList.add('yellow');
//         } else {
//             cell.classList.remove('red', 'yellow');
//         }
//     });

//     if (isGameEnded) {
//         // Handle the end of the game
//     }
// }
