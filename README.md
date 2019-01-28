### Redesign orders.html

to better display on smaller viewports/windows

Consider stacking all elements

Try updating calculation code (process.py) with Pandas, like [here](https://colab.research.google.com/drive/1sgXlv-CC59RpirS5R63y3dvYYL-Cz4_Y)

## Log

* Added to directory .htaccess file:

```
<Files orders.html>
	Header set Cache-Control "no-cache, no-store, must-revalidate"
	Header set Pragma "no-cache"
	Header set Expires "0"
</Files>
```
