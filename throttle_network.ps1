param(
    [string]$action
)

# Define your Wi-Fi adapter name (you can get it by running `Get-NetAdapter`)
$adapter = "Wi-Fi"

if ($action -eq "throttle") {
    Write-Host "Throttling Wi-Fi speed..."
    
    # Set a low bandwidth limit (e.g., 1 Mbps)
    netsh interface ipv4 set subinterface "$adapter" throttling=enabled
    netsh interface ipv4 set subinterface "$adapter" bandwidth=1
}
elseif ($action -eq "restore") {
    Write-Host "Restoring Wi-Fi speed..."
    
    # Remove throttling
    netsh interface ipv4 set subinterface "$adapter" throttling=disabled
    netsh interface ipv4 set subinterface "$adapter" bandwidth=0
}
