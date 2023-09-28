import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Cloud Surge",
  description: "Massively parallel computation of chemical spaces in cloud environments with Surge",
  base: "/cloud-surge/",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Docs', link: '/introduction' }
    ],

    logo: '/surge-logo.png',

    siteTitle: '',

    sidebar: [
      {
        text: 'Welcome',
        items: [
          { text: 'Introduction', link: '/introduction' },
          { text: 'Architecture', link: '/architecture' },
          { text: 'Sustainability', link: '/sustainability' },
        ]
      },
      {
        text: 'Installation',
        items: [
          { text: 'Docker', link: '/docker' },
          { text: 'Cluster Deployment (K8S)', link: '/deployment' },
          { text: 'Scaling', link: '/scaling' },
          { text: 'Filters', link: '/filters' },
          { text: 'Screening', link: '/screening' },
        ]
      },
     // {
      //   text: 'Google Cloud - GKE',
      //   items: [
      //     { text: 'Guides', link: '/guides' },
      //   ]
      // },
      // {
      //   text: 'Analysis',
      //   items: [
      //     { text: 'Datasets', link: '/datasets' },
      //     { text: 'Formats', link: '/formats' },
      //     { text: 'Runtimes', link: '/runtimes' },
      //   ]
      // },
      {
        text: 'Development',
        items: [
          { text: 'Local Installation', link: '/installation' },
          { text: 'GitHub Actions', link: '/actions' },
          { text: 'Contributors', link: '/contributors' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Steinbeck-Lab/cloud-surge' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2023-present Steinbeck Lab'
    }
  }
})
