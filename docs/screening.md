# Screen structures

Screening large chemical databases is a common task in various fields, including drug discovery, materials science, and chemical informatics.

Storing the large datasets generated and screening them in principle sounds sensible but in view of efficiency its always advisable to screen these structures as and when they are generated and store only a subset of data making it more managable.

Jobs submitted to the kubernetes can use microservice such as Cheminformatics Microservice to filter the generated structures based on criteria such as Natural Product Likeliness Scores and/or others.

Cheminformatics Microservice: Enables you to effortlessly integrate cheminformatics tools into your web application or workflows.

https://github.com/Steinbeck-Lab/cheminformatics-microservice

job.yaml update

```
- name: cheminformatics-microservice
    image: nfdi4chem/cheminformatics-microservice:lite
    imagePullPolicy: Always
```

example filtering of natural product like molecules

```
url = "http://localhost:80/latest/chem/nplikeness/score?smiles=" + quote(smiles)
nplikeness_score = float(requests.request("GET", url).text)
if 0 <= nplikeness_score + 2.31 <= 7.46:
```

Note: adding these additional filters might increase the runtimes of your jobs but they could also potentially reduce the amount of data generated. Please pay attention to the filters and make a choice on how to optimise your workflow.
