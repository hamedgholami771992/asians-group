Write-Host 'Starting full Django database reset...' -ForegroundColor Cyan

# 1. Remove database file
if (Test-Path 'db.sqlite3') {
    Remove-Item 'db.sqlite3' -Force
    Write-Host 'Removed db.sqlite3' -ForegroundColor Green
} else {
    Write-Host 'db.sqlite3 not found, skipping...' -ForegroundColor Yellow
}

# 2. Remove old migration files except __init__.py
$dirs = @('.\subscriptions\migrations', '.\accounts\migrations')
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Get-ChildItem -Path $dir -Include *.py,*.pyc -Recurse |
            Where-Object { $_.Name -ne '__init__.py' } |
            Remove-Item -Force
        Write-Host "Cleaned migrations from $dir" -ForegroundColor Green
    } else {
        Write-Host "Migration folder not found: $dir - skipping..." -ForegroundColor Yellow
    }
}

# 3. Recreate migrations
Write-Host 'Creating new migrations...' -ForegroundColor Cyan
python manage.py makemigrations accounts
python manage.py makemigrations subscriptions

# 4. Apply migrations
Write-Host 'Applying migrations...' -ForegroundColor Cyan
python manage.py migrate


Write-Host ''
Write-Host 'Reset completed successfully!' -ForegroundColor Green
