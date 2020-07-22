# -*- Gets Machine IP address, Netmask, DNS and prefix
function Get-ServerIPAddress {
    $IPType = "IPv4"
    $IPv4Address = $(Get-NetAdapter | ? {$_.Status -eq "up"}| Get-NetIPAddress | ? {$_.AddressFamily -eq "IPv4"}).IPv4Address
    $Prefix = $(Get-NetAdapter | ? {$_.Status -eq "up"} | Get-NetIPAddress).PrefixLength[1]
    $Gateway = "$((Get-WmiObject Win32_NetworkAdapterConfiguration -EA Stop | ? {$_.IPEnabled}).DefaultIPGateway)"
    $DNS = $(Get-NetAdapter | ? {$_.Status -eq "up"} | Get-DnsClientServerAddress | ? {$_.AddressFamily -eq 2}).ServerAddresses
    return $IPType, $IPv4Address, $Prefix, $Gateway, $DNS
  }

Write-Output(Get-ServerIPAddress)