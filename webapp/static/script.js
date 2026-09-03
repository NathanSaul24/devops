function doSignup() {
    let username = document.getElementById("username_box").value;
    let password = document.getElementById("password_box").value;

    fetch("/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password })
    })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            if (data.ok) {
                showLoggedIn(data.username);
            } else {
                alert(data.error);
            }
        });
}

function doLogin() {
    let username = document.getElementById("username_box").value;
    let password = document.getElementById("password_box").value;

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password })
    })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            if (data.ok) {
                showLoggedIn(data.username);
            } else {
                alert(data.error);
            }
        });
}

function doLogout() {
    fetch("/logout", { method: "POST" })
        .then(function () {
            document.getElementById("login_area").style.display = "block";
            document.getElementById("logged_in_area").style.display = "none";
            document.getElementById("stats_area").innerText = "";
        });
}

function showLoggedIn(username) {
    document.getElementById("login_area").style.display = "none";
    document.getElementById("logged_in_area").style.display = "block";
    document.getElementById("logged_in_username").innerText = username;
}

function showStats() {
    fetch("/stats")
        .then(function (response) { return response.json(); })
        .then(function (data) {
            let statsBox = document.getElementById("stats_area");
            statsBox.innerHTML =
                "Games played: " + data.games_played + "<br>" +
                "Average time: " + data.average_seconds + " seconds<br>" +
                "Longest win: " + data.longest_win + "s, shortest win: " + data.shortest_win + "s<br>" +
                "Longest loss: " + data.longest_loss + "s, shortest loss: " + data.shortest_loss + "s";
        });
}

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