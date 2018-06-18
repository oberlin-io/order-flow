### Redesign orders.html

to better display on smaller viewports/windows

Consider stacking all elements

## Log

* Added to directory .htaccess file:

```
<Files orders.html>
	Header set Cache-Control "no-cache, no-store, must-revalidate"
	Header set Pragma "no-cache"
	Header set Expires "0"
</Files>
```