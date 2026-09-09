$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $root 'backend'
$frontendDir = Join-Path $root 'frontend\frontend'
$pythonExe = Join-Path $backendDir '.venv\Scripts\python.exe'
$backendUrl = 'http://127.0.0.1:8000'
$frontendUrl = 'http://127.0.0.1:5173'

if (-Not (Test-Path $pythonExe)) {
    Write-Error "Python environment not found at $pythonExe. Please set up the backend venv first."
    exit 1
}

if (-Not (Test-Path $frontendDir)) {
    Write-Error "Frontend folder not found at $frontendDir."
    exit 1
}

$backendCommand = "cd `"$backendDir`"; & `"$pythonExe`" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"
$frontendCommand = "cd `"$frontendDir`"; npm install; npm run dev"

$wt = Get-Command wt.exe -ErrorAction SilentlyContinue
if ($wt) {
    $args = @(
        'new-tab',
        'powershell',
        '-NoExit',
        '-Command',
        $backendCommand,
        ';',
        'split-pane',
        '-H',
        'powershell',
        '-NoExit',
        '-Command',
        $frontendCommand
    )

    Start-Process wt.exe -ArgumentList $args
    Write-Host "Starting backend and frontend..."
    Write-Host "Backend: $backendUrl"
    Write-Host "Frontend: $frontendUrl"
    return
}

Write-Host "Starting backend first..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand

$deadline = (Get-Date).AddSeconds(30)
while ((Get-Date) -lt $deadline) {
    try {
        $response = Invoke-WebRequest -Uri $backendUrl -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) { break }
    }
    catch {
        Start-Sleep -Milliseconds 500
    }
}

Write-Host "Starting frontend..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand
Write-Host "Both services are starting. Backend: $backendUrl"
Write-Host "Frontend: $frontendUrl"