$triggerDaily = New-ScheduledTaskTrigger -Daily -At 8:30PM
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn
Set-ScheduledTask -TaskName "AutoPostDaily60Days" -Trigger @($triggerDaily, $triggerLogon)
Write-Output "Task triggers updated successfully!"
