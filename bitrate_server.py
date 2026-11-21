import functools
import http.server
import os
import socketserver
import threading
import obspython as obs

PORT = 8011
HTML_FILE_PATH = ""
SERVER_THREAD = None
HTTP_SERVER = None


class QuietBitrateHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # 避免頻繁請求造成 OBS 腳本記錄洗版
        pass


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def _run_server(directory: str, port: int):
    global HTTP_SERVER
    handler = functools.partial(QuietBitrateHandler, directory=directory)
    try:
        with ReusableTCPServer(("127.0.0.1", port), handler) as httpd:
            HTTP_SERVER = httpd
            obs.script_log(
                obs.LOG_INFO,
                f"[Bitrate Server] 已啟動：http://localhost:{port}/bitrate.html"
            )
            httpd.serve_forever()
    except Exception as e:
        obs.script_log(obs.LOG_ERROR, f"[Bitrate Server] 啟動失敗：{e}")
    finally:
        HTTP_SERVER = None


def start_server_for_html(html_path: str):
    stop_server()

    if not html_path or not os.path.isfile(html_path):
        obs.script_log(obs.LOG_WARNING, "[Bitrate Server] 請先選擇有效的 bitrate.html 檔案。")
        return

    target_dir = os.path.dirname(os.path.abspath(html_path))
    global SERVER_THREAD
    SERVER_THREAD = threading.Thread(
        target=_run_server,
        args=(target_dir, PORT),
        daemon=True,
    )
    SERVER_THREAD.start()


def stop_server():
    global HTTP_SERVER, SERVER_THREAD
    if HTTP_SERVER is not None:
        try:
            HTTP_SERVER.shutdown()
            HTTP_SERVER.server_close()
            obs.script_log(obs.LOG_INFO, "[Bitrate Server] 已停止 HTTP 伺服器。")
        except Exception as e:
            obs.script_log(obs.LOG_WARNING, f"[Bitrate Server] 停止伺服器時發生問題：{e}")
        HTTP_SERVER = None
    SERVER_THREAD = None


def script_description():
    return (
        "<h2>Bitrate HTML 本機伺服器</h2>"
        "<p>選擇 <b>bitrate.html</b> 所在位置後，自動於本機 <b>8011</b> 埠啟動伺服器。</p>"
        "<p>可在瀏覽器來源輸入：<code>http://localhost:8011/bitrate.html</code></p>"
    )


def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(
        props,
        "bitrate_html_path",
        "選擇 bitrate.html 位置",
        obs.OBS_PATH_FILE,
        "HTML Files (*.html *.htm);;All Files (*.*)",
        None,
    )
    obs.obs_properties_add_button(
        props,
        "restart_btn",
        "重新啟動 8011 伺服器",
        lambda props, prop: (start_server_for_html(HTML_FILE_PATH), False)[1],
    )
    return props


def script_update(settings):
    global HTML_FILE_PATH
    new_path = obs.obs_data_get_string(settings, "bitrate_html_path")
    if new_path != HTML_FILE_PATH or HTTP_SERVER is None:
        HTML_FILE_PATH = new_path
        start_server_for_html(HTML_FILE_PATH)


def script_unload():
    stop_server()