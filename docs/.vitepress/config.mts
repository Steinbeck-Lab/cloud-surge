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
          { text: 'Formulae', link: '/formulae' },
          { text: 'Filters', link: '/filters' },
          { text: 'Screening', link: '/screening' },
        ]
      },
     {
        text: 'Google Cloud - GKE',
        items: [
          { text: 'Guides', link: '/google-cloud-gke/guides',
            items: [
              { text: 'Setup', link: '/google-cloud-gke/guides',
              items: [
                { text: 'Project', link: '/google-cloud-gke/create-google-cloud-project' },
                { text: 'Cluster', link: '/google-cloud-gke/create-cluster' },
                { text: 'Workspace', link: '/google-cloud-gke/clone-project' },
                { text: 'Service Account', link: '/google-cloud-gke/create-service-account' },
                { text: 'Storage', link: '/google-cloud-gke/create-bucket' },
              ],
            },
              { text: 'Cloud Surge-Jobs', link: '/google-cloud-gke/launch-cloud-surge' },
              { text: 'Output', link: '/google-cloud-gke/access-result' },
              { text: 'Delete', link: '/google-cloud-gke/delete-everything' },
            ]
          },
        ]
      },
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
      message: 'Cloud-Surge: Code and configurations released under the MIT License | Surge: Source code released under Apache License 2.0 <br/> Funded by the <a href="https://www.dfg.de/en/index.jsp" style="color: blue" target="_blank">Deutsche Forschungsgemeinschaft (DFG, German Research Foundation)</a> under the <a href="https://www.nfdi4chem.de/" style="color: blue" target="_blank">National Research Data Infrastructure – NFDI4Chem</a> – Project number: 441958208',
      copyright: `Copyright © ${new Date().getFullYear()} Steinbeck Lab`
    }
  }
})
