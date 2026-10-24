# NEXT TOKEN website

Static site for NEXT TOKEN: an about page (`site/index.html`) and the web build (`site/play.html`, game in
`site/game/`). No build step; GitHub Pages publishes `site/` on push to `main`.

Update the game: run `tools/export_web.sh` in `next-token`, then `tools/update_game.sh` here, commit, push.
Screenshots in `site/img/` are Movie Maker frames from the game.
