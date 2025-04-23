function createBoard() {
    const board = [];
    for (let i = 0; i < 4; i++) {
        board.push([0, 0, 0, 0]);
    }
    return board;
}

function addRandomTile(board) {
    let empty = [];
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            if (board[i][j] === 0) empty.push([i, j]);
        }
    }

    if (empty.length === 0) return board;

    const [r, c] = empty[Math.floor(Math.random() * empty.length)];
    board[r][c] = Math.random() < 0.9 ? 2 : 4;

    return board;
}

function combineRow(row) {
    let newRow = row.filter(x => x !== 0);
    for (let i = 0; i < newRow.length - 1; i++) {
        if (newRow[i] === newRow[i + 1]) {
            newRow[i] *= 2;
            newRow[i + 1] = 0;
        }
    }
    newRow = newRow.filter(x => x !== 0);
    while (newRow.length < 4) newRow.push(0);
    return newRow;
}

function reverse(board) {
    return board.map(row => row.reverse());
}

function transpose(board) {
    return board[0].map((_, i) => board.map(row => row[i]));
}

function moveLeft(board) {
    return board.map(row => combineRow(row));
}

function moveRight(board) {
    return reverse(moveLeft(reverse(board)));
}

function moveUp(board) {
    return transpose(moveLeft(transpose(board)));
}

function moveDown(board) {
    return transpose(moveRight(transpose(board)));
}

function checkWin(board) {
    for (let row of board) {
        if (row.includes(2048)) {
            return true;
        }
    }
    return false;
}

function checkLose(board) {
    // If there is at least one empty cell, not lost
    for (let row of board) {
        if (row.includes(0)) return false;
    }

    // If any adjacent tiles can merge (horizontally or vertically), not lost
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            if (j < 3 && board[i][j] === board[i][j + 1]) return false;
            if (i < 3 && board[i][j] === board[i + 1][j]) return false;
        }
    }

    return true;
}

let board = addRandomTile(addRandomTile(createBoard()));

document.addEventListener("keydown", function (e) {
    const keyMap = {
        ArrowUp: moveUp,
        ArrowDown: moveDown,
        ArrowLeft: moveLeft,
        ArrowRight: moveRight
    };
    const moveFn = keyMap[e.key];
    if (moveFn) {
        const newBoard = moveFn(board.map(row => [...row]));
        if (JSON.stringify(newBoard) !== JSON.stringify(board)) {
            board = addRandomTile(newBoard);
            updateBoard(board);
        }

        if (checkWin(board)) {
                document.getElementById("message").textContent = "You won!";
            } else if (checkLose(board)) {
                document.getElementById("message").textContent = "Game Over!";
            }
    }
});

document.getElementById("restart").addEventListener("click", () => {
    board = addRandomTile(addRandomTile(createBoard()));
    updateBoard(board);
    document.getElementById("message").textContent = "";
});

function updateBoard(board) {
    const boardDiv = document.getElementById("board");
    boardDiv.innerHTML = "";
    board.forEach(row => {
        row.forEach(cell => {
            const cellDiv = document.createElement("div");
            cellDiv.className = "cell";
            if (cell !== 0) {
                cellDiv.textContent = cell;
                cellDiv.setAttribute("data-val", cell);
            }
            boardDiv.appendChild(cellDiv);
        });
    });
}

updateBoard(board);