param ($puzlnum, $uniq=1)

$sttm = Get-Date

C:\Users\Fitzs\PycharmProjects\RushHour\venv\Scripts\python.exe C:/Users/Fitzs/PycharmProjects/RushHour/PuzzleN4j.py ${puzlnum} ${uniq}

$entm = Get-Date
echo "Puzzle ${puzlnum} started  ${sttm}"
echo "Puzzle ${puzlnum} completed ${entm}"
