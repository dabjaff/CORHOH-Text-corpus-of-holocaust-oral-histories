# CORHOH: Text Corpus of Holocaust Oral Histories

**CORHOH (Text CORpus of HOlocaust Oral Histories)** is a standardized dataset comprising **500 oral histories** from Holocaust survivors. These narratives were retrieved via the Let Them Speak Project and sourced from the United States Holocaust Memorial Museum (USHMM). The corpus has been normalized, enriched with detailed metadata, and encoded in a TEI-based XML format aligned with **Text Encoding Initiative (TEI)** guidelines (TEI Consortium 2023) to support research in linguistics, history, psychology, and digital humanities.

---

## What’s New in This Version

This release is a **modified version** of an earlier CORHOH build. In the previous version, **one survivor’s oral history appeared twice** (two oral histories included under the 500-record set). In this version:

- **Each of the 500 records corresponds to exactly one oral history (one survivor → one oral history).**
- As a result of this correction, the **global totals of turns changed**:
  - **Questions:** 106,702  
  - **Answers:** 107,305  

A corresponding revision note is recorded in the TEI header (`<revisionDesc>`).

---

## Technical Features & Data Quality

### TEI-Based Header Standardization

The corpus includes a standardized TEI header to improve interoperability and long-term preservation:

- **`<fileDesc>`**: Bibliographic and publication metadata (title, publication statement, source description)
- **`<revisionDesc>`**: Version history and corpus-level modifications (including the correction described above)
- (Where applicable in earlier/alternate builds) **`<profileDesc>`**: Descriptive profiling such as abstracts  

*Note:* CORHOH versions may differ in whether the abstract is placed under `<publicationStmt>` or `<profileDesc>`. The “with_header_and_note_v2” style places the abstract within `<publicationStmt>`.

### “Ultra Clean” Character Encoding

An “Ultra Clean” normalization pass was applied to remove legacy character-encoding artifacts that typically arise from mixed encodings (e.g., Mac Roman, Windows-1252, UTF-8 misreads). Examples of fixes include:

- **Apostrophes & quotes:** normalization of corrupted characters into standard `'` and `"` where possible
- **Dashes:** replacement of dash artifacts with standard hyphen/en dash/em dash where appropriate
- **Special characters:** correction of common mojibake sequences and replacement characters

This improves downstream search, NLP processing, and reproducibility across platforms.

---

## Corpus Structure

### Record-Level Organization

The XML structure is:

- `<TEI xmlns="http://www.tei-c.org/ns/1.0">`
  - `<teiHeader> ... </teiHeader>`
  - `<CORHOH>`
    - repeated `<text id="...">` (500 records)

Each record contains:

1) **Oral History Details** (`<Oral_History_Details>`)
- Document ID (USHMM reference)
- Recording date
- Recording length
- Question/Answer ID ranges
- Permission type
- USHMM catalog link

2) **Individual Metadata** (`<Individual_Meta_Data>`)
- Name, DOB, gender, birthplace
- Ghetto and camp history (if available)
- Immigration date and destination (if available)

### Transcript Annotation

Transcripts are encoded as dialogue turns:

- **`<div type="question">`** interviewer question
- **`<div type="answer">`** survivor response
- Each turn contains:
  - `<speaker role="interviewer|interviewee">Q… / A…</speaker>`
  - `<u> ... </u>` (utterance text)

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
            <Imm_Date>1949</Imm_Date>
            <Imm_Destination>USA</Imm_Destination>
        </Individual_Meta_Data>
    </meta>
    <text>
        <body>
            <div type="interview">
                <head>Interview Transcript</head>
                <div type="question">
                    <speaker role="interviewer">Q1</speaker>
                    <u>Please tell me where you were born and when and a little bit about your family.</u>
                </div>
                <div type="answer">
                    <speaker role="interviewee">A1</speaker>
                    <u>I was born in Lodz, Poland.</u>
                </div>
            </div>
        </body>
    </text>
</text>
```

---

## Data Access & Validation

- **Mendeley Data Repository:** https://data.mendeley.com/datasets/gz7v268252/2  
- **Validation:** An XSD schema is distributed alongside the XML to support structural validation of the CORHOH TEI-based format.

---

## License & Ethical Use

CORHOH is sourced from USHMM public collections. Usage must comply with USHMM terms and ethical guidelines. The corpus is distributed under:

- **CC BY-NC-SA 4.0**

USHMM terms of use:  
https://www.ushmm.org/copyright-and-legal-information/terms-of-use

---

## Citation

If you use CORHOH in your research, please cite:

Jaff, D. Q. (2025). CORHOH: Text corpus of Holocaust oral histories. *Data in Brief, 59*, 111426.  
DOI: https://doi.org/10.1016/j.dib.2025.111426
