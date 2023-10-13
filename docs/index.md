---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: Cloud Surge
  text: Massively parallel computation of chemical spaces in cloud environments with
    Surge
  tagline:
  image:
    src: /header.png
    alt: Cloud Surge - Structure Generation
  actions:
    - theme: brand
      text: Documentation
      link: /introduction
    - theme: alt
      text: Docker Images
      link: https://hub.docker.com/r/nfdi4chem/cloud-surge

features:
  - icon: 🛠️
    title: Parallel Job Pattern - External work queue
    details: Supports reliable parallel execution of Pods, where each Pod can work
      in a set of independent but related work items.
  - icon: 💻
    title: Cloud-Agnostic Deployment Solution
    details: A versatile deployment solution that enables Surge to be seamlessly deployed
      on any K8S cloud service providers, offering flexibility.
  - icon: 🌍
    title: Efficient Resource Optimization
    details: A sustainable approach to cloud computing that optimizes solution efficiency,
      minimizes resource wastage.
  - icon: 📚
    title: Comprehensive Documentation and Guides
    details: Extensive and user-friendly documentation with step-by-step guides to
      assist users in understanding and extending the solution to its fullest potential.
---
