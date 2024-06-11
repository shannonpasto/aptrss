# aptrss
### An RSS feed generator for apt upgradeable packages
Generate a [W3C valid](https://validator.w3.org/feed/) rss feed for apt upgradeable packages. It first runs `apt update` then takes the output of `apt list --upgradable`.

To configure, just set `url_origin` which is your full url, eg `https://www.myserver.com`, save and run. You can also set the following optional variables...

`url_pathname` - the url subdirectory or file, defaults to `index.html`

`file_path` - path to your www directory and file, defaults to `/var/www/html/index.html`

`feed_name` - set the feed title, defaults to `Apt Upgradeable Packages`

Run regularly using cron.

Enjoy!
