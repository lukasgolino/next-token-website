#!/usr/bin/env bash
# Copy the game's web build (../next-token/build/web, made by its tools/export_web.sh) into site/game.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
src="${1:-$here/../next-token/build/web}"
rm -rf "$here/site/game"
mkdir -p "$here/site/game"
cp "$src"/index.* "$here/site/game/"
# Tag the game page with the site's analytics (Cloudflare Web Analytics beacon + Umami): it's also opened on its own, outside play.html.
python3 - "$here/site/game/index.html" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
tag = ("<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
       "data-cf-beacon='{\"token\": \"1c2ae262b9034043ac24d179d34c8a27\"}'></script>\n"
       "<script defer src=\"https://cloud.umami.is/script.js\" data-website-id=\"6c3ba9da-9af9-49a9-a575-90c9cace445c\" data-auto-track=\"false\"></script>\n"
       # play.html frames this page: count a view only when it is opened on its own, not inside play.html
       "<script>addEventListener(\"load\", () => { if (window.top === window.self && window.umami) umami.track(); });</script>\n</body>")
assert s.count("</body>") == 1, "game/index.html: expected one </body>"
open(p, "w", encoding="utf-8").write(s.replace("</body>", tag))
PY
echo "copied $(du -sh "$here/site/game" | cut -f1) from $src"
