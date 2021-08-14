$noOfCars = 2
for($i = 0; $i  -le $noOfCars; $i++){ 
	start cmd -ArgumentList {/c python sub.py}
	$sleepFor = Get-Random -Maximum 20
	Start-Sleep -seconds $sleepFor
}