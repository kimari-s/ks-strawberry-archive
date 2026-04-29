# ks-strawberry-archive

Archive of the CGI scripts from あやしいわーるど＠ストロベリー / ＠なごみ, a BBS active circa 2011–2017.

## Base

- くずはすくりぷと + ＠くずは萌え ver1.1.1
- ks_treeview, ks_imode
- ずるぼんあぷろだ（ゆいのーと + ずるぼん + 擬古描 + しばカウンタ 2001年10月27日版）

## Structure

```
index.cgi        Main BBS script (Perl CGI, Shift_JIS)
                   - File attachment (integrated with uploader)
                   - Twitter integration (Net::Twitter::Lite, bidirectional)
                   - Spam scoring with silent drop
                   - Per-user customization via bit-packed cookies
                   - Thumbnail embedding (YouTube, Niconico, Amazon)
sub/             Perl modules
  bbsadmin.pl      Admin tools
  bbslog.pl        Log viewer
  bbscust.pl       User settings UI
  ks_treeview.pl   Threaded tree view
  ks_imode.pl      Mobile (i-mode/EZweb) support
  upload.pl        File upload handler
  ust.pl           Ustream live status integration
jcode.pl         Character encoding library
up/index.cgi     Uploader (ずるぼん-derived)
ust/index.cgi    Ustream status page
res/             Icons and images
info.htm         Copyright / access keys
```

## Notes

- This is an archive for reference, not intended for reuse
- API keys and site-specific values are replaced with `REDACTED`
- Source encoding is Shift_JIS (cp932)

## Related

- [nss](https://github.com/kimari-s/nss) — PHP + MySQL rewrite (successor)
