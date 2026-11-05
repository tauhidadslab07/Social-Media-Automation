$task = Get-ScheduledTask -TaskName "AutoPostDaily60Days"
$settings = $task.Settings
$settings.StartWhenAvailable = $true
$settings.DisallowStartIfOnBatteries = $false
$settings.StopIfGoingOnBatteries = $false
$settings.WakeToRun = $true
Set-ScheduledTask -TaskName "AutoPostDaily60Days" -Settings $settings
Write-Output "Successfully updated Task Scheduler with StartWhenAvailable, WakeToRun, and Battery settings!"
