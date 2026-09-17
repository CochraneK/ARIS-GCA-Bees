param(
    [string]$ArisRoot = "$HOME/aris_repo",
    [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot/..").Path,
    [switch]$SkipSkillUpdate,
    [switch]$AttachProject
)

$ErrorActionPreference = "Stop"
$upstream = "https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is required."
}

if (-not (Test-Path "$ArisRoot/.git")) {
    Write-Host "Cloning ARIS into $ArisRoot"
    git clone $upstream $ArisRoot
} else {
    Write-Host "Updating ARIS in $ArisRoot"
    git -C $ArisRoot fetch --tags origin
    git -C $ArisRoot pull --ff-only origin main
}

$commit = (git -C $ArisRoot rev-parse HEAD).Trim()
$tag = (git -C $ArisRoot describe --tags --abbrev=0 2>$null)
if (-not $tag) { $tag = "unreleased" }
$tag = $tag.Trim()

Write-Host "ARIS synced: $tag ($commit)"

$bash = Get-Command bash -ErrorAction SilentlyContinue
if (-not $SkipSkillUpdate) {
    if ($bash) {
        Push-Location $ArisRoot
        try {
            Write-Host "Running ARIS smart skill update..."
            bash tools/smart_update.sh --apply --add-new
        }
        finally {
            Pop-Location
        }
    } else {
        Write-Warning "bash not found. Upstream repo is updated, but smart_update.sh was not run. Use Git Bash/WSL or ARIS-Code CLI."
    }
}

if ($AttachProject) {
    if (-not $bash) {
        throw "Project attachment requires bash (Git Bash/WSL)."
    }
    Push-Location $ArisRoot
    try {
        Write-Host "Attaching project-local ARIS skills to $ProjectRoot"
        bash tools/install_aris.sh "$ProjectRoot"
    }
    finally {
        Pop-Location
    }
}

$localState = @{
    upstream = $upstream
    tag = $tag
    commit = $commit
    synced_at = (Get-Date).ToString("o")
    aris_root = $ArisRoot
} | ConvertTo-Json
$localState | Set-Content -Encoding UTF8 (Join-Path $ProjectRoot "aris.local.json")

Write-Host "Local state written to aris.local.json (gitignored)."
Write-Host "For a new paper, copy the exact tag + commit into that paper's paper.json before the ARIS run."
