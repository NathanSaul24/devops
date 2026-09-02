let gameIsOver = false;

function drawBoard(boardString) {
    for (let i = 0; i < 9; i++) {
        let square = document.getElementById("spot_" + (i + 1));
        let letter = boardString[i];
        if (letter === "_") {
            square.innerText = "";
        } else {
            square.innerText = letter;
        }
    }
}

function showMessage(status) {
    let messageBox = document.getElementById("message");
    if (status === "O_WINS") {
        messageBox.innerText = "You win!";
        gameIsOver = true;
    } else if (status === "X_WINS") {
        messageBox.innerText = "You lose!";
        gameIsOver = true;
    } else if (status === "DRAW") {
        messageBox.innerText = "It's a draw!";
        gameIsOver = true;
    } else if (status === "BAD_MOVE") {
        messageBox.innerText = "That spot is taken, try another one.";
    } else {
        messageBox.innerText = "";
    }
}

function playerClicked(spot) {
    if (gameIsOver) {
        return;
    }

    fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ spot: spot })
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            drawBoard(data.board);
            showMessage(data.status);
        });
}

function startNewGame() {
    fetch("/new_game", { method: "POST" })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            gameIsOver = false;
            drawBoard(data.board);
            document.getElementById("message").innerText = "";
        });
}