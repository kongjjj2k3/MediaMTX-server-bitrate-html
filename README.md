# MediaMTX-server-bitrate-html
![GitHub top language](https://img.shields.io/github/languages/top/kongjjj2k3/MediaMTX-server-bitrate-html?&style=for-the-badge)
[![Downloads](https://img.shields.io/github/downloads/kongjjj2k3/MediaMTX-server-bitrate-html/total?label=Downloads&style=for-the-badge&color=lightgreen)](https://github.com/kongjjj2k3/MediaMTX-server-bitrate-html/releases)

##### HTML for OBS overlay that shows current bitrate of MediaMTX RTMP & SRT servers.

---
使用設定：
1. OBS bitrate overlay網址：http://127.0.0.1:8080/Bitrate.html
2. 修改MediaMTX Control API , api: true
3. MediaMTX apiAllowOrigins：只允許 http://127.0.0.1:8080,將
apiAllowOrigins: []
改成
apiAllowOrigins:
  - http://127.0.0.1:8080
4. 將Start_Bitrate_Server.bat 啟動檔，放在 Bitrate.html 同一個資料夾(請將下載的Bitrate_EN.html改名成Bitrate.html)，
雙擊 Start_Bitrate_Server.bat。看到 HTTP Server 啟動後，OBS bitrate overlay就可以使用。

---
### Please download it in [HTML](https://github.com/masarujp2022/MediaMTX-server-bitrate-html/tree/main/HTML) directory or [Releases](https://github.com/kongjjj2k3/MediaMTX-server-bitrate-html/releases) page.
---
