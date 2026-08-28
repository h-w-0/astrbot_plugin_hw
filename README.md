# astrbot_plugin_hw

自用插件

## 功能

- 指令：`/hw` 或 `/HW`
- 调用接口 `https://hw233.cn/api/RandomOC.php` 获取随机赠图及信息
- 回复内容：图片 + 日期、作者、ID 信息
- 支持**群聊白名单**配置

## 安装

1. 将本插件文件夹 `astrbot_plugin_hw` 放入 AstrBot 的 `data/plugins` 目录
2. 在 AstrBot WebUI → 插件管理中启用本插件
3. （可选）在插件配置中设置群聊白名单

## 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `group_whitelist` | 群聊白名单。不填（空列表）则默认对所有群聊和私聊开放；填写群号后，仅白名单内的群可使用 `/hw` 指令 | `[]` |

在 WebUI 插件配置页面可直接编辑白名单列表，填入 QQ 群号即可。

## 回复示例

```
[图片]
2026-04-16 by 信长白羽
ID 39
```

## 依赖

- aiohttp（异步 HTTP 请求）

## 开发参考

- [AstrBot 插件开发指南](https://docs.astrbot.app/dev/star/plugin-new.html)
- [消息发送](https://docs.astrbot.app/dev/star/guides/send-message.html)
- [插件配置](https://docs.astrbot.app/dev/star/guides/plugin-config.html)

使用了Grok制作
