param(
  [Parameter(Mandatory=$true)][string]$DrawioPath,
  [string]$OutDir = "",
  [string]$DrawioExe = "",
  [double]$Scale = 1.5,
  [switch]$NoPdf,
  [switch]$EmbedPngDiagram
)

$ErrorActionPreference = "Stop"

function Resolve-DrawioExe {
  param([string]$Candidate)
  if ($Candidate -and (Test-Path -LiteralPath $Candidate)) {
    return (Resolve-Path -LiteralPath $Candidate).Path
  }
  if ($env:DRAWIO_EXE -and (Test-Path -LiteralPath $env:DRAWIO_EXE)) {
    return (Resolve-Path -LiteralPath $env:DRAWIO_EXE).Path
  }
  $cmd = Get-Command "draw.io.exe","drawio.exe","draw.io" -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($cmd) { return $cmd.Source }
  $common = @(
    "D:\drawio\draw.io\draw.io.exe",
    "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe",
    "$env:ProgramFiles\draw.io\draw.io.exe",
    "${env:ProgramFiles(x86)}\draw.io\draw.io.exe"
  )
  foreach ($p in $common) {
    if ($p -and (Test-Path -LiteralPath $p)) { return (Resolve-Path -LiteralPath $p).Path }
  }
  throw "draw.io executable not found. Set DRAWIO_EXE or pass -DrawioExe."
}

$drawio = Resolve-DrawioExe -Candidate $DrawioExe
$input = (Resolve-Path -LiteralPath $DrawioPath).Path
if (-not $OutDir) {
  $OutDir = Split-Path -Parent $input
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$base = [System.IO.Path]::GetFileNameWithoutExtension($input)
$png = Join-Path $OutDir "$base.png"
$svg = Join-Path $OutDir "$base.svg"
$pdf = Join-Path $OutDir "$base.pdf"

if ($EmbedPngDiagram) {
  & $drawio --export --format png --embed-diagram --output $png --scale $Scale $input
} else {
  & $drawio --export --format png --output $png --scale $Scale $input
}
& $drawio --export --format svg --embed-diagram --output $svg $input
if (-not $NoPdf) {
  & $drawio --export --format pdf --embed-diagram --output $pdf $input
}

Start-Sleep -Seconds 2
Get-ChildItem -LiteralPath $OutDir -Filter "$base.*" |
  Select-Object FullName, Length, LastWriteTime |
  Format-Table -AutoSize
