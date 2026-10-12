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

推送到 `main` 分支即触发 GitHub Actions，构建并部署到 GitHub Pages（`actions/deploy-pages`）。

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
