# 瑞士中国商会 · Swiss Chinese Enterprises Association

基于 [VitePress](https://vitepress.dev/) 构建的瑞士中国商会官网重构版。内容来自原站 `https://www.swisscea.com/`（WordPress）。

## 页面

- `/` 首页（Hero / 会员单位 / 协会新闻）
- `/about` 关于我们
- `/members` 会员企业
- `/contact` 联系我们
- `/news/` 协会新闻（列表）
- `/news/{id}` 新闻文章 × 12

## 本地开发

```bash
npm install
npm run docs:dev      # 本地开发服务器
npm run docs:build    # 构建到 docs/.vitepress/dist
npm run docs:preview  # 预览构建产物
```

## 部署

推送 `main` 中的网站内容（`docs/`）、依赖、新闻列表生成脚本或部署工作流时，自动构建并部署到 GitHub Pages。仅修改 README、测试或导入工具不触发网站构建。快速连续推送会取消旧的构建任务；正在执行的部署不会被中断，过期的网站产物会跳过发布。

### 导入微信公众号新闻

在 Actions 中打开 **Import WeChat article to SCEA news → Run workflow**，选择 `main`，在 `article_ids` 输入文章短 ID 或 `https://mp.weixin.qq.com/s/<ID>` 链接，多篇以空格或换行分隔。

- 已存在的文章会跳过，不重复下载，也不重新构建。需要修改已有文章时直接编辑对应 Markdown 并推送。
- 新文章逐篇在临时目录导入。抓取、正文或日期校验失败时，整批不会提交、发布，Actions会报错；修复来源后可重试。
- 成功后由机器人提交文章和图片，再**显式调用唯一的部署工作流**，自动生成首页和新闻目录、构建并发布。机器人默认令牌的推送不会再次触发推送工作流，因此每批新内容只调用一次构建。
- 导入工具或工作流更新不再自动重试旧的固定文章。发布流程也可通过 **Deploy VitePress site to Pages → Run workflow** 手动重试，无需重新导入。

依赖安装使用 npm 下载缓存；Pages构建产物只保留1天。没有删除既有图片、文章或Git历史。

> ⚠️ 需在仓库 `Settings → Pages` 中将 **Source** 设为 **GitHub Actions**，并在 **Custom domain** 填入 `www.swisscea.com`。

### 路径约定（换域名不失效）

- `base` 为默认 `/`（自定义域名根路径）。
- Markdown 文章内链接用**相对地址**（`about`、`news/218`…）。
- 图片用 `/img/…`（VitePress public 资源约定，跟随域名自动解析），由 VitePress 自动处理。

因此无论部署到 `www.swisscea.com` 还是任意域名/子路径，都无需改动内容。

## 资产来源

图片原文件下载自原站 `wp-content/uploads`，存放于 `docs/public/img/`：

- `logo.png` 商会标志
- `hero.jpg` 首页横幅
- `ICBC / constructionbank / HUAWEI / AIRCHINA / casic / boc / chinamobile .png` 会员单位标志
