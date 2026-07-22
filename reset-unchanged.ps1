$diff = git diff --stat HEAD^0
$lines = $diff -split '\r?\n'

$unchanged = @()
foreach ($line in $lines) {
    if ($line -like "*2 +-") {
        $parts = $line -split '\|'
        $fileName = $parts[0].Trim()
        $unchanged += $fileName
    }
}
Write-Host $unchanged
git reset $unchanged
