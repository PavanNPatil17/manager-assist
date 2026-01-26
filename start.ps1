Write-Host "Starting Cortex Deployment..." -ForegroundColor Cyan

Write-Host "`nCreating virtual environment with uv..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists, skipping creation." -ForegroundColor Green
} else {
    uv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
uv pip install -r pyproject.toml
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "`nBuilding manager-chat image..." -ForegroundColor Yellow
langgraph build -t manager-chat
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to build manager-chat image" -ForegroundColor Red
    exit 1
}

Write-Host "`nStarting Docker services..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start Docker services" -ForegroundColor Red
    exit 1
}

Write-Host "`nWaiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host "`nService Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host "`nDeployment complete!" -ForegroundColor Green
Write-Host "`nServices available at:" -ForegroundColor Cyan
Write-Host "  - LangGraph API: http://localhost:8123" -ForegroundColor White
Write-Host "  - Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  - Milvus: http://localhost:19530" -ForegroundColor White
Write-Host "  - PostgreSQL: localhost:5432" -ForegroundColor White
Write-Host "  - Redis: localhost:6379" -ForegroundColor White
Write-Host "`nTo view logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "To stop services: docker-compose down" -ForegroundColor Yellow
