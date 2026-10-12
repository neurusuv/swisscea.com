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

> ⚠️ 需在仓库 `Settings → Pages` 中将 **Source** 设为 **GitHub Actions**。

### 站点路径（base）

当前 `docs/.vitepress/config.mts` 中 `base: '/swisscea.com/'`，对应项目 Pages 地址 `https://<owner>.github.io/swisscea.com/`。若改用自定义域名（如 `swisscea.com`），把 `base` 改为 `'/'` 并重新提交即可。

## 资产来源

图片原文件下载自原站 `wp-content/uploads`，存放于 `docs/public/img/`：

- `logo.png` 商会标志
- `hero.jpg` 首页横幅
- `ICBC / constructionbank / HUAWEI / AIRCHINA / casic / boc / chinamobile .png` 会员单位标志
