export function drawBestMove(boardAPI, bestMove, quality) {
  if (!boardAPI || !bestMove) return

  const from = bestMove.slice(0, 2)
  const to = bestMove.slice(2, 4)

  const colors = {
    best: 'green',
    good: 'blue',
    inaccuracy: 'yellow',
    mistake: 'orange',
    blunder: 'red',
  }

  boardAPI.drawMove(from, to, colors[quality] || 'green')
}

export function clearArrows(boardAPI) {
  if (boardAPI) boardAPI.hideMoves()
}
