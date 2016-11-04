% from etc import cfg
<html>
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="/static/style.css">
        <title>Bibliothèque</title>
        <script src="/static/brython/brython.js"></script>
    </head>

    <body onload="brython({{cfg['general']['Debug']}})">
        {{!corps}}
    </body>
</html>
