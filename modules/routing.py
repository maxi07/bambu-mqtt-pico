from modules.Microdot.microdot import send_file, Response, redirect
from modules.Microdot.utemplate import Template
import modules.settings as settings
from modules.logging import *
import gc
import sys
import ure as re


Response.default_content_type = 'text/html'


@settings.app.get("/images/<path:path>")
async def get_image(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    if str(path).endswith('.svgz'):
        log_info("Sending compressed svgz:", path)
        return send_file('images/' + path, compressed=True, content_type="image/svg+xml", max_age=86400)
    elif str(path).endswith('.ico'):
        return send_file('images/' + path, max_age=86400, content_type="image/x-icon")
    else:
        return send_file('images/' + path, max_age=86400)


@settings.app.get("/css/styles.css")
async def get_css(request):
    return send_file('css/styles.css', max_age=86400)


@settings.app.get("/scripts/<string:scriptname>")
async def get_js(request, scriptname):
    if str(scriptname).endswith('.js'):
        return send_file('scripts/' + scriptname, max_age=86400)


@settings.app.get('/')
async def index(request):
    try:
        log_info("Sending root site to client")
        version = settings.config.get('version', 'unknown')
        micropython_version = get_micropython_version()
        return await Template('index.html').render_async(micropython_version=micropython_version,
                                                         version=version)
    except Exception as e:
        import sys
        sys.print_exception(e)  # type: ignore
        log_error("Failed loading HTML site.", e)
        body = "Failed loading site." + str(e)
        return body, 500, {'Content-Type': 'text/html'}
    finally:
        gc.collect()


@settings.app.post('/api/settings')
async def post_api_settings(request):
    try:
        log_info("Received settings update.")
        new_access_code = request.form.get('accessCode')
        log_info("Received new access code:", new_access_code)
        settings.config.set('printer.password', new_access_code)
        return redirect('/')
    except Exception as e:
        import sys
        sys.print_exception(e)  # type: ignore
        log_error("Failed updating settings.", e)
        return Response(status_code=500)


def register_routes():
    log_info("Microdot routes loaded.")


def get_micropython_version() -> str:
    try:
        micropython_version: str = sys.version
        match = re.search(r"v\d+\.\d+\.\d+", micropython_version)
        if match:
            micropython_version = match.group(0)
    except Exception as e:
        log_error("Unable to read MicroPython version.", e)
    finally:
        return micropython_version
