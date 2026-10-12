import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  base: '/swisscea.com/',
  title: '瑞士中国商会',
  description:
    '瑞士中国商会（Swiss Chinese Enterprises Association）是根据瑞士法律成立的自愿非营利组织，搭建中瑞企业经贸合作的桥梁平台。',
  head: [
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    [
      'link',
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap',
      },
    ],
    ['link', { rel: 'icon', type: 'image/png', href: '/img/logo.png' }],
    ['meta', { name: 'theme-color', content: '#B80E1E' }],
    ['meta', { property: 'og:site_name', content: '瑞士中国商会' }],
    ['meta', { property: 'og:locale', content: 'zh_CN' }],
  ],
  appearance: false,
  cleanUrls: true,
  lastUpdated: false,
  markdown: {
    theme: { light: 'github-light', dark: 'github-dark' },
  },
})
