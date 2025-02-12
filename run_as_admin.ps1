param (
    [string]$action
)

$cache_dir = "C:\Squid\var\cache"
$squid_config = "C:\Squid\etc\squid.conf"

if ($action -eq "throttle") {
    # Update Squid configuration to throttle bandwidth
    (Get-Content $squid_config) -replace 'delay_parameters 1 6250000/6250000
', 'delay_parameters 1 8000/8000' | Set-Content $squid_config
} elseif ($action -eq "restore") {
    # Restore normal bandwidth
    (Get-Content $squid_config) -replace 'delay_parameters 1 8000/8000', 'delay_parameters 1 6250000/6250000
' | Set-Content $squid_config
}

# Restart Squid to apply changes
Stop-Service squid
Start-Service squid
