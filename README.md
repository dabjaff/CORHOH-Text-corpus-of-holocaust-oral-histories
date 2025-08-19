# CORHOH: Text Corpus of Holocaust Oral Histories

This repository hosts documentation and related resources for **CORHOH (Text CORpus of HOlocaust Oral Histories)**. The corpus brings together **500 Holocaust survivor oral histories** from the United States Holocaust Memorial Museum (USHMM), normalized, annotated, and enriched with detailed metadata for use in linguistic, historical, psychological, and computational research. The raw text of each file is copied from Let them Speak project (https://lts.fortunoff.library.yale.edu/about).

---

## Example Record

```xml
<text id="RG-50.462.0010">
    <meta>
        <Oral_History_Details>
            <Documents_ID>RG-50.462.0010</Documents_ID>
            <Rec_Date>1985</Rec_Date>
            <Rec_Length>75</Rec_Length>
            <A_Number>A1-A121</A_Number>
            <Q_Number>Q1-Q120</Q_Number>
            <permission_type>No restrictions</permission_type>
            <Link>https://collections.ushmm.org/search/catalog/irn508631</Link>
        </Oral_History_Details>
        <Individual_Meta_Data>
            <Name>Anatole Gorko</Name>
            <DOB>1907</DOB>
            <Gender>M</Gender>
            <Born>Poland</Born>
            <Ghetto>nan</Ghetto>
            <Camp>Auschwitz</Camp>
            <Imm_Date>1948</Imm_Date>
            <Imm_Destination>USA</Imm_Destination>
        </Individual_Meta_Data>
    </meta>
    <text>
</text>
```

---

## Corpus Overview

- **Size:** 500 oral histories  
- **Total Questions:** 106,519  
- **Total Answers:** 107,125  
- **Format:** XML with schema definition (XSD), compliant with [Text Encoding Initiative (TEI)](https://tei-c.org) standards  
- **Annotation:** Each oral history contains structured transcripts distinguishing between interviewer questions and survivor answers  

The corpus is designed to support research across multiple disciplines, including linguistics, history, cultural studies, psychology, and digital humanities.

---

## Data Files  

The corpus is distributed in two separate archives for convenience:  

- **Q.zip** → Contains all **questions** asked by interviewers (`Q1, Q2, ... Qn`)  
- **A.zip** → Contains all **answers** given by Holocaust survivors (`A1, A2, ... An`)  


This separation allows researchers to:  
- Focus exclusively on **interviewer discourse** (Q)  
- Analyze only **survivor narratives** (A)  
- Or combine both for full **dialogue reconstruction**  

---

## Data Access  

The full dataset is openly available via **Mendeley Data**:  

- **Mendeley Data – DOI:** [10.17632/gz7v268252.2](https://data.mendeley.com/datasets/gz7v268252/2)  

All corpus files are distributed in **XML** format with accompanying **XSD** schema for validation.  

---

## Reference  

If you use CORHOH in your research, please cite:  

> Jaff, D.Q. (2025). CORHOH: Text corpus of Holocaust oral histories. *Data in Brief, 59*, 111426. [https://doi.org/10.1016/j.dib.2025.111426](https://doi.org/10.1016/j.dib.2025.111426)  

---

## License  

The CORHOH corpus is distributed under the [Creative Commons BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
