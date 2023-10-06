# Formulae

Surge is a command-line generator of chemical structures. It is written in a portable subset of the C language and runs on any computer that can run nauty. The only compulsory input is a chemical formula. 

```
surge -u C8H11NO
>Z generated 17379 -> 500039 -> 2123287 in 0.12 sec 1 Here surge has reported that it found 2,123,287 molecules in 0.12 seconds.
```

## Formulae Generator

You can generate the formulae up to the give number of heavy atoms using the following commands

- Generate class file

```
javac -cp ~/Downloads/commons-cli-1.5.0.jar:~/Downloads/cdk-2.9.jar FormulaGenerator.java
```

- Run formulae generator

```
java -cp .:~/commons-cli-1.5.0.jar:~/Downloads/cdk-2.9.jar FormulaGenerator.class -heavyAtoms 7 -path ~/Downloads
```

All the jar files are available in the resources/formulae/FormulaeGenerator.zip