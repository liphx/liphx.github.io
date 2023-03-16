---
title: 申请letsencrypt ssl证书
date: 2024-03-05
tags: tools
---

```shell
pip3 install --upgrade certbot
sudo certbot --text --agree-tos --email lipenghua@lipenghua.com -d '*.lipenghua.com' --manual --preferred-challenges dns --expand --renew-by-default certonly
```
