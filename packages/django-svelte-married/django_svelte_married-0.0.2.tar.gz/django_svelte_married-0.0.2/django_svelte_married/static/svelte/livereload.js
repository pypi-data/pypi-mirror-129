function randHash() {
    return (Math.random() + 1).toString(36).substring(7);
}

function handleMessage(m) {
    const { command, path } = m;
    if (command === "reload") {
        if (path.endsWith(".js") || path.endsWith(".jsx") || path.endsWith(".ts") || path.endsWith(".svelte")) {
            for (const script of document.querySelectorAll("script[src][svelte-livereload]")) {
                const parentNode = script.parentNode;
                const scriptCopy = document.createElement("script");
                scriptCopy.setAttribute("svelte-livereload", "true");
                scriptCopy.src = script.src;
                script.parentNode.removeChild(script);
                parentNode.appendChild(scriptCopy);
            }
        } else if (path.endsWith(".css") || path.endsWith(".scss")) {
            for (const el of document.querySelectorAll("link[rel=\"stylesheet\"][svelte-livereload]")) {
                const href = el.getAttribute('href');
                el.setAttribute('href', href.split("?")[0] + "?v=" + randHash());
            }
        } else if (path.endsWith(".html")) {
            top.window.location.reload();
        }
    } else {
        console.debug(m);
    }
}

const client = new WebSocket(window['SVELTE_LIVERELOAD_PORT'] || "ws://localhost:5050/livereload");
client.onopen = function() { client.send(JSON.stringify({command: "hello"})) }
client.onmessage = function (e) { handleMessage(JSON.parse(e.data)) }
client.onclose = function() { top.window.location.reload() }
