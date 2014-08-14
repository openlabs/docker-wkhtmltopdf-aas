import base64
import json
import tempfile
from werkzeug.wrappers import Request, Response
from executor import execute


@Request.application
def application(request):
    """
    To use this application, the user must send a POST request with
    base64 encoded HTML content and the wkhtmltopdf Options in
    request data, with keys 'base64_html' and 'options'.
    The application will return a response with the PDF file.
    """
    if request.method != 'POST':
        return

    with tempfile.NamedTemporaryFile(
        suffix='.html', prefix='trytond_', delete=False
    ) as source_file:
        options = json.loads(request.form['options'])
        file_name = source_file.name
        source_file.write(base64.b64decode(request.form['base64_html']))
        source_file.close()

        # Evaluate argument to run with subprocess
        args = '/usr/local/bin/wkhtmltopdf.sh'
        # Add Global Options
        if options:
            for option, value in options.items():
                args += ' --%s' % option
                if value:
                    args += ' "%s"' % value

        # Add source file name and output file name
        args += ' %s %s.pdf' % (file_name, file_name)
        # Execute the command using executor
        execute(args)
        return Response(base64.b64encode(open(file_name + '.pdf').read()))

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        '127.0.0.1', 5000, application, use_debugger=True, use_reloader=True
    )
