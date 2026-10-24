<script setup lang="ts">
import { useData, useRoute, withBase } from 'vitepress'
import { computed, ref, onMounted, watch } from 'vue'

const { frontmatter, title } = useData()
const route = useRoute()

const isHome = computed(() => frontmatter.value.layout === 'home')
const isJoin = computed(() => route.path === '/join' || route.path === '/join.html')
const isNewsArticle = computed(() => /^\/news\/[^/]+(?:\.html)?$/.test(route.path))

const nav = [
  { label: '首页', path: '/' },
  { label: '关于我们', path: '/about' },
  { label: '会员企业', path: '/members' },
  { label: '联系我们', path: '/contact' },
  { label: '协会新闻', path: '/news/' },
]

const href = (p: string) => withBase(p)

const isActive = (p: string) => {
  if (p === '/') return route.path === '/' || route.path === '/index'
  return route.path.startsWith(p.replace(/\/$/, ''))
}

const menuOpen = ref(false)
const scrolled = ref(false)

const onScroll = () => {
  scrolled.value = window.scrollY > 8
}

onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
})

watch(
  () => route.path,
  () => {
    menuOpen.value = false
  }
)
</script>

<template>
  <div class="sc-shell" :class="{ 'is-home': isHome }">
    <header class="sc-nav" :class="{ 'is-scrolled': scrolled }">
      <div class="sc-nav__inner">
        <a class="sc-brand" :href="href('/')" aria-label="瑞士中国商会 首页">
          <img class="sc-brand__logo" src="/img/logo.png" alt="瑞士中国商会" width="44" height="44" />
          <span class="sc-brand__text">
            <span class="sc-brand__cn">瑞士中国商会</span>
            <span class="sc-brand__en">Swiss Chinese Enterprises Association</span>
          </span>
        </a>

        <nav class="sc-links" aria-label="主导航">
          <a
            v-for="item in nav"
            :key="item.path"
            class="sc-links__item"
            :class="{ 'is-active': isActive(item.path) }"
            :href="href(item.path)"
          >{{ item.label }}</a>
          <a class="sc-links__cta" :href="href('/join')">加入我们</a>
        </nav>

        <button
          class="sc-burger"
          :aria-expanded="menuOpen"
          aria-label="打开菜单"
          @click="menuOpen = !menuOpen"
        >
          <span></span><span></span><span></span>
        </button>
      </div>

      <transition name="drop">
        <nav v-if="menuOpen" class="sc-drawer" aria-label="移动端导航">
          <a
            v-for="item in nav"
            :key="item.path"
            :class="{ 'is-active': isActive(item.path) }"
            :href="href(item.path)"
          >{{ item.label }}</a>
          <a class="sc-drawer__cta" :href="href('/join')">加入我们</a>
        </nav>
      </transition>
    </header>

    <main class="sc-main">
      <Content
        v-if="!isHome"
        class="sc-page"
        :class="{ 'sc-page--join': isJoin, 'sc-page--news': isNewsArticle }"
      />
      <Content v-else class="sc-home" />
    </main>

    <footer class="sc-footer">
      <div class="sc-footer__inner">
        <div class="sc-footer__brand">
          <img src="/img/logo.png" alt="瑞士中国商会" width="52" height="52" />
          <div>
            <p class="sc-footer__name">瑞士中国商会</p>
            <p class="sc-footer__sub">Swiss Chinese Enterprises Association</p>
          </div>
        </div>

        <nav class="sc-footer__nav" aria-label="页脚导航">
          <a :href="href('/about')">关于我们</a>
          <a :href="href('/members')">会员企业</a>
          <a :href="href('/contact')">联系我们</a>
          <a :href="href('/join')">加入商会</a>
          <a :href="href('/news/')">协会新闻</a>
        </nav>

        <div class="sc-footer__contact">
          <p>微信公众号：瑞士中国商会</p>
          <p>邮箱：<a href="mailto:info@swisscea.com">info@swisscea.com</a></p>
        </div>
      </div>
      <div class="sc-footer__legal">
        <span>© 2024 瑞士中国商会 · 保留所有权利</span>
      </div>
    </footer>
  </div>
</template>
