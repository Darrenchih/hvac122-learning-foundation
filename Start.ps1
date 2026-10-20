param([int]$Port = 8122, [switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$webRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'app'))
$listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $Port)
try { $listener.Start() } catch { Write-Error "Cannot bind 127.0.0.1:$Port. Close the previous instance or use -Port 8123. $_"; exit 1 }
$url = "http://127.0.0.1:$Port/"
Write-Host "HVAC-122 offline review: $url"
Write-Host 'Keep this window open. Press Ctrl+C to stop. No administrator rights required.'
if (-not $NoBrowser) { Start-Process $url }
try {
 while ($true) {
  $client = $listener.AcceptTcpClient()
  try {
   $client.ReceiveTimeout = 3000
   $client.SendTimeout = 3000
   $stream = $client.GetStream()
   $reader = [IO.StreamReader]::new($stream, [Text.Encoding]::ASCII, $false, 1024, $true)
   $line = $reader.ReadLine()
   if (-not $line) { continue }
   do { $headerLine = $reader.ReadLine() } while ($null -ne $headerLine -and $headerLine.Length -gt 0)
   $parts = $line.Split(' ')
   $relative = [Uri]::UnescapeDataString(($parts[1].Split('?')[0])).TrimStart('/')
   if (-not $relative) { $relative = 'index.html' }
   # Deliberate allow-list: source materials and local learning records are never served.
   if ($parts[0] -ne 'GET' -or $relative -notin @('index.html','style.css','bank.js','core.js','app.js','content.js','content-loader.js','manage.html','manage.js','materials.js')) {
    $status = '404 Not Found'; $bytes = [Text.Encoding]::UTF8.GetBytes('Not found'); $mime = 'text/plain'
   } else {
    $status = '200 OK'; $bytes = [IO.File]::ReadAllBytes((Join-Path $webRoot $relative))
    $mime = switch ([IO.Path]::GetExtension($relative)) { '.html' {'text/html'} '.css' {'text/css'} '.js' {'text/javascript'} default {'application/octet-stream'} }
   }
   $response = "HTTP/1.1 $status`r`nContent-Type: $mime; charset=utf-8`r`nContent-Length: $($bytes.Length)`r`nCache-Control: no-store`r`nConnection: close`r`nX-Content-Type-Options: nosniff`r`n`r`n"
   $head = [Text.Encoding]::ASCII.GetBytes($response)
   $stream.Write($head,0,$head.Length); $stream.Write($bytes,0,$bytes.Length); $stream.Flush()
  } catch { Write-Warning "Request failed: $($_.Exception.Message)" } finally { $client.Dispose() }
 }
} finally { $listener.Stop() }
