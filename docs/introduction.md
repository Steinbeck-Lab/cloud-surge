---
outline: deep
---

<p align="center">
  <img class="only-on-light" align="center" src="/cloud-surge.png#gh-dark-mode-only" alt="Cloud Surge Logo" style="filter: drop-shadow(0px 0px 10px rgba(0, 0, 0, 0.5)); width:40vw">
</p>
<p align="center">
  <img class="only-on-dark" align="center" src="/cloud-surge-light.png#gh-dark-mode-only" alt="Cloud Surge Logo" style="filter: drop-shadow(0px 0px 10px rgba(0, 0, 0, 0.5)); width:40vw">
</p>

<hr/>

# Introduction

In the realm of drug discovery, compound libraries and databases play a vital role. The initial phase of drug development heavily relies on the diversity and size of these sets of compounds. The discovery of new compounds is primarily based on combining known molecular building blocks or substructures in a combinatorial manner. However, a significant constraint is the limited size of these compound libraries. To address these limitations, computational methods are employed to explore the vast chemical landscape, generating an array of molecular structures with diverse features. As an alternative to existing databases, one approach involves generating all possible structures for given molecular formulas, tailoring a specific molecular dataset to meet researchers' needs.

Chemical graph generation presents a formidable challenge in the field of computer-assisted structure elucidation (CASE). Starting with the pioneering DENDRAL study, numerous chemical graph generators were developed. Nonetheless, many of these encountered limitations due to the exponential increase in heavy atom combinations. For a long time, MOLGEN held the status of the gold standard software in terms of speed and reliability until the emergence of the Surge algorithm. Surge stands out as the fastest chemical graph generator, with additional features slated for future releases. The development of such a rapid open-source generator prompts the question: How can we build extensive compound libraries using Surge?

There are already computationally constructed molecular databases in existence. Reymond contributed three significant compound databases: GDB11, GBD13, and GDB 17. These databases were constructed based on an upper limit for the total number of heavy atoms, as indicated by their names, and adhered to chemical constraints to ensure the molecules were chemically meaningful. For instance, GDB11 contains molecular structures with up to 11 heavy atoms in total. The numbers indicate the upper limits. GDB13 is the largest publicly available small molecule database, containing 977,46,314 molecules. Although GDB17 has around 166 billion molecules, it is not entirely publicly accessible; only a subset of GDB17 with 50 million molecules can be accessed.

Surge excels in its ability to perform fast, duplicate-free, and efficient structure generation. To expedite this structure generation a step further, we present Cloud Surge, that harnesses the immense computational power of cloud environments coupled with the efficiency of Surge.

The storage of these large databases represents another significant challenge in the construction process. An effective solution for storage leveraging cloud systems, such as the Google Cloud Storage (buckets) is also integrated here. The generated set of molecules can be stored in cloud environments and made available as publicly accessible databases. 

In addition to the Surge plugin system, which allows users to add new functionalities (chemical constraints according to their requirements) to Surge by incorporating their plugin classes. We also present an approach to screen generated structures before storage there by avoiding the necessity to store all enumerated structures.

Consequently, Surge stands out as the most efficient software for building extensive databases, offering options to blacklist/screen certain chemical constraints. With Cloud Surge, large and extensive compound libraries can be explored efficiently.