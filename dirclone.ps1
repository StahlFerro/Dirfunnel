function Show-Menu {
    [string]$Title = 'Dirclone' 
    [string]$version = '0.0.1'
    Write-Host "=============================== $Title v$version ==============================="
    Write-Host "1. List target directories"
    Write-Host "2. List save directory"
    Write-Host "3. Add/update target directory"
    Write-Host "4. Remove target directory"
    Write-Host "5. Add/update save directory"
    Write-Host "6. Copy target directories into save directory (existing overwrite)"
    Write-Host "7. Show python version"
}

do {
    venv\Scripts\Activate.ps1;
    Show-Menu;
    $input = Read-Host "Please enter a number. Enter q to quit";
    Write-Host
    switch ($input) {
        '1' { python main.py list }
        '2' { python main.py save-info }
        '3' {
            $name = Read-Host "Enter designation name"
            $path = Read-Host "Enter target directory path"
            if (!($name -eq '' -OR $path -eq '')){
                python main.py add $name $path
            }
            else { Write-Host "Please do not leave one or more of the arguments blank!" }
        }
        '4' {
            $name = Read-Host "Enter designation name"
            if (!($name -eq '')){
                python main.py remove $name
            }
            else { Write-Host "Please do not leave one or more of the arguments blank!" }
        }
        '5' {
            $path = Read-Host "Enter save directory"
            if (!($name -eq '')){
                python main.py set-save $path
            }
            else { Write-Host "Please do not leave one or more of the arguments blank!" }
        }
        '6' { python main.py clone }
        '7' { python --version }
        'q' { venv\Scripts\deactivate.bat; return; }
        Default {}
    }
    Write-Host
    Pause
}
until ($input -eq 'q')
