$action = New-ScheduledTaskAction -Execute "c:\Users\HP\Documents\antigravity\optimistic-brahmagupta\run_post.bat" -WorkingDirectory "c:\Users\HP\Documents\antigravity\optimistic-brahmagupta"
$triggerDaily = New-ScheduledTaskTrigger -Daily -At 8:30PM
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun -DontStopOnIdleEnd

Register-ScheduledTask -TaskName "AutoPostDaily60Days" -Action $action -Trigger @($triggerDaily, $triggerLogon) -Settings $settings -Force

Write-Output "Successfully updated AutoPostDaily60Days with Dual Triggers (Daily 8:30 PM + AtLogOn) and Battery support!"
