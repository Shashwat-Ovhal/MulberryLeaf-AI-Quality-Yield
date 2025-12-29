$ErrorActionPreference = "Stop"
$ProjectPath = "c:\Users\Shashwat\OneDrive\Desktop\MulberryLeaf-AI-Quality-Yield\mobile"

if (!(Test-Path $ProjectPath)) {
    New-Item -ItemType Directory -Path $ProjectPath
}

Set-Location $ProjectPath
Write-Output "Initializing Expo in $ProjectPath..."
npx create-expo-app@latest . --template blank --no-install --yes

Write-Output "Installing dependencies..."
npm install axios expo-image-picker expo-camera lucide-react-native expo-constants expo-linking expo-status-bar
