# =====================================================================
#  backup_snapshot.ps1
#  app.py 등 핵심 파일이 저장될 때마다 안전한 스냅샷 백업을 남긴다.
#  - 정전/강제종료로 작업 중 파일이 깨져도 직전 안전본을 항상 복구 가능.
#  - 폴더명은 기존 방식(_backup_MMDD_HHMM)을 유지한다.
#  - 원자적 복사(임시파일 -> 교체)로 복사 도중 종료돼도 백업본이 깨지지 않는다.
#  - .autobackup 표식이 있는 폴더만 정리(prune) 대상 -> 수동 백업은 절대 삭제 안 함.
# =====================================================================
$ErrorActionPreference = 'Stop'

$root = $PSScriptRoot
if (-not $root) { $root = Split-Path -Parent $MyInvocation.MyCommand.Path }

# 백업할 핵심 파일 (있는 것만 복사)
$files = @(
    'app.py',
    'bookings.json',
    'version_counter.json',
    'requirements.txt',
    'Dockerfile',
    '.dockerignore',
    '.firebaserc',
    'firebase.json',
    'run.bat',
    'run_app.bat'
)

# 하루(날짜)당 보관할 자동 백업 개수
$KEEP_PER_DAY = 30

$stamp = Get-Date -Format 'MMdd_HHmm'
$dest  = Join-Path $root "_backup_$stamp"

if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest | Out-Null
}

# 자동 백업 표식 (정리 시 이 표식이 있는 폴더만 삭제)
Set-Content -LiteralPath (Join-Path $dest '.autobackup') -Value $stamp -Encoding utf8

foreach ($f in $files) {
    $src = Join-Path $root $f
    if (Test-Path -LiteralPath $src) {
        $final = Join-Path $dest $f
        $tmp   = "$final.tmp"
        # 원자적 복사: 임시 파일에 먼저 쓴 뒤 교체
        Copy-Item -LiteralPath $src -Destination $tmp -Force
        Move-Item -LiteralPath $tmp -Destination $final -Force
    }
}

# 오래된 자동 백업 정리 (.autobackup 표식이 있는 폴더만).
# 날짜(MMDD)별로 묶어, 각 날짜마다 최근 $KEEP_PER_DAY 개만 남기고 나머지 삭제.
$autoBackups = Get-ChildItem -LiteralPath $root -Directory -Filter '_backup_*' -ErrorAction SilentlyContinue |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName '.autobackup') }

$autoBackups |
    Group-Object { if ($_.Name -match '^_backup_(\d{4})_') { $Matches[1] } else { 'unknown' } } |
    ForEach-Object {
        $_.Group |
            Sort-Object LastWriteTime -Descending |
            Select-Object -Skip $KEEP_PER_DAY |
            ForEach-Object {
                Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
            }
    }
