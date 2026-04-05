#!/usr/bin/perl


require '../sub/ust.pl';
$ust_cache = './channel.cache';
$ust_cachetime = 20;
$table = &ust_maketable;

if($msg){ $msg = "<p>$msg</p>"; }

print <<EOF;
Content-type: text/html

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="../res/sw_ust_favicon.ico">
<title>REDACTED</title>
<style type="text/css">
<!--
  .list td a { text-decoration: none; }
  .list td a:hover {text-decoration: none; background-color: #508080; color: #FFFFFF;}
  img { border: none; }
  ul {margin:0 auto;}
-->
</style>
</head>
<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">

<div align="center">

<h3>REDACTED</h3>

<hr>

<p>
<small>
<a href="http://www.ustream.tv/" target="_blank">USTREAM</a>
| <a href="https://twitter.com/#!/REDACTED" target="_blank">\@REDACTED</a>
| <a href="REDACTED" target="_blank">住人Stream一覧</a>
</small>
</p>

<table><tr><td>
<small>
<ul>
<li>住人のUSTチャンネルリストです</li>
<li>ツイッター<a href="https://twitter.com/#!/REDACTED" target="_blank">\@REDACTED</a>にて配信情報の通知を行なっています</li>
<li>リストへの追加・削除の要請は<a href="https://twitter.com/#!/REDACTED" target="_blank">\@REDACTED</a>か<a href="REDACTED" target="_blank">掲示板</a>へどうぞ</li>
</ul>
</small>
</td></tr></table>

<p>
<a href="https://twitter.com/REDACTED" class="twitter-follow-button" data-show-count="false" data-lang="ja">\@REDACTEDをフォロー</a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
</p>

$msg

$table
<br>

<hr>
</div>

<div align="right">
<a href="REDACTED" target="_blank">＠USTREAM</a>
</div>

</body>
</html>
EOF

exit;

sub err{
	print "Content-type: text/plain\n\n$_[0]";
	exit;
}