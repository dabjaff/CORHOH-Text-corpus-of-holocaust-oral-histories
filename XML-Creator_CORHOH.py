"""CORHOH TEI/XML creator"""

from __future__ import annotations
import argparse
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple
import pandas as pd
from xml.sax.saxutils import escape



DEFAULT_METADATA_CSV = "Cor_META_updated.csv"
DEFAULT_TEXTS_DIR = "500_numbered"
DEFAULT_OUTPUT_XML = "CORHOH.xml"


@dataclass(frozen=True)
class Indent:
    """Indentation policy for pretty output."""

    CORHOH: str = "    "
    TEXT: str = "        "
    L2: str = "            "
    L3: str = "                "
    L4: str = "                    "
    L5: str = "                        "
    L6: str = "                            "


IND = Indent()

_Q_RE = re.compile(r"^\s*Q(\d+)\s*:\s*(.*)\s*$")
_A_RE = re.compile(r"^\s*A(\d+)\s*:\s*(.*)\s*$")


def configure_logging(verbosity: int) -> None:
    """Map -v/-vv to logging levels."""
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def smart_read(path: Path) -> str:
    """Read transcript text with a pragmatic encoding fallback and cleanup.

    We first try UTF-8 (with BOM support), then fall back to cp1252 and replace
    common legacy corruption artifacts observed in this dataset.
    """

    raw = path.read_bytes()
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        content = raw.decode("cp1252", errors="replace")
    replacements = {
        "Õ": "'",
        "Ô": "'",
        "Ò": '"',
        "Ó": '"',
        "Ñ": "—",
        "‹": "ã",
        "√ït": "'t",
        "√ïs": "'s",
        "√ïll": "'ll",
        "√ï": "'",
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)

    return content


def fixed_header_block(total_q: int, total_a: int, nl: str = "\n") -> str:
    """Create the TEI header block with dynamic Q/A counts."""

    abstract_text = (
        "CORHOH (Text Corpus of Holocaust Oral Histories) comprises 500 oral histories "
        "from Holocaust survivors, with each narrative retrieved via the Let Them Speak "
        "Project (Toth 2021). The corpus has been processed and enriched with metadata "
        "describing both the testimony givers and the interviews. Non-content technical "
        "material has been removed, and each interviewer question and survivor answer "
        "has been assigned a unique identifier. The corpus follows TEI guidelines "
        "(TEI Consortium 2023). In this version, the dataset contains "
        f"{total_q} questions and {total_a} answers, providing a substantial "
        "interdisciplinary resource for research in the humanities and social sciences. "
        "CORHOH is sourced from the United States Holocaust Memorial Museum (USHMM) "
        "and is publicly available under a CC BY-NC-SA 4.0 license."
    )

    return (
        f"{IND.CORHOH}<teiHeader>{nl}"
        f"{IND.TEXT}<fileDesc>{nl}"
        f"{IND.L2}<titleStmt>{nl}"
        f"{IND.L3}<title>CORHOH: Text Corpus of Holocaust Oral Histories</title>{nl}"
        f"{IND.L3}<respStmt>{nl}"
        f"{IND.L4}<resp>Mendeley Repository: https://data.mendeley.com/datasets/gz7v268252/2</resp>{nl}"
        f"{IND.L3}</respStmt>{nl}"
        f"{IND.L2}</titleStmt>{nl}"
        f"{IND.L2}<publicationStmt>{nl}"
        f"{IND.L3}<publisher>Data in Brief: https://www.sciencedirect.com/science/article/pii/S2352340925001581</publisher>{nl}"
        f"{IND.L3}<date>2025</date>{nl}"
        f"{IND.L3}<availability>{nl}"
        f"{IND.L4}<licence>All data used in this study comply with ethical guidelines of the United States Holocaust Memorial Museum (https://www.ushmm.org/copyright-and-legal-information/terms-of-use), and the oral histories included in the CORHOH corpus are publicly available under the CC BY-NC-SA 4.0 license.</licence>{nl}"
        f"{IND.L3}</availability>{nl}"
        f"{IND.L2}</publicationStmt>{nl}"
        f"{IND.L2}<sourceDesc>{nl}"
        f"{IND.L3}<bibl>{nl}"
        f"{IND.L4}<title>CORHOH</title>{nl}"
        f"{IND.L4}<author>Daban Q. Jaff</author>{nl}"
        f"{IND.L4}<pubPlace>Universität Erfurt, Philosophische Fakultät</pubPlace>{nl}"
        f"{IND.L4}<date>2025</date>{nl}"
        f"{IND.L3}</bibl>{nl}"
        f"{IND.L3}<p>Data collected from oral history interviews from Let Them Speak: https://lts.fortunoff.library.yale.edu/about</p>{nl}"
        f"{IND.L2}</sourceDesc>{nl}"
        f"{IND.TEXT}</fileDesc>{nl}"
        f"{IND.TEXT}<profileDesc>{nl}"
        f"{IND.L2}<abstract>{escape(abstract_text)}</abstract>{nl}"
        f"{IND.TEXT}</profileDesc>{nl}"
        f"{IND.TEXT}<revisionDesc>{nl}"
        f"{IND.L2}<change when=\"2025-02-01\">Initial TEI encoding applied.</change>{nl}"
        f"{IND.L2}<change when=\"2026-01-19\">Modified release: corrected a duplicate inclusion; this version contains one oral history per survivor across the 500 records. Counts updated to {total_q} questions and {total_a} answers.</change>{nl}"
        f"{IND.TEXT}</revisionDesc>{nl}"
        f"{IND.CORHOH}</teiHeader>{nl}"
    )


Turn = Tuple[str, str, str]


def parse_transcript_to_turns(text: str) -> List[Turn]:

    turns: List[Turn] = []
    cur_type: str | None = None
    cur_label: str | None = None
    cur_buf: List[str] = []

    def flush() -> None:
        nonlocal cur_type, cur_label, cur_buf
        if cur_type is None:
            return
        turns.append((cur_type, cur_label or "", "\n".join(cur_buf).strip()))

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        m_q = _Q_RE.match(line)
        m_a = _A_RE.match(line)

        if m_q:
            flush()
            cur_type = "question"
            cur_label = "Q" + m_q.group(1)
            cur_buf = [m_q.group(2)]
            continue

        if m_a:
            flush()
            cur_type = "answer"
            cur_label = "A" + m_a.group(1)
            cur_buf = [m_a.group(2)]
            continue

        if cur_type is not None:
            cur_buf.append(line)

    flush()
    return turns


def build_record_xml(row: Dict[str, str], transcript_text: str, nl: str = "\n") -> Tuple[str, int, int]:
   

    def field(key: str) -> str:
        return escape(str(row.get(key, "")).strip())

    doc_id = field("Documents ID")
    turns = parse_transcript_to_turns(transcript_text)

    div_blocks: List[str] = []
    for ttype, label, utt in turns:
        role = "interviewer" if ttype == "question" else "interviewee"
        div_blocks.append(
            f"{IND.L5}<div type=\"{ttype}\">{nl}"
            f"{IND.L6}<speaker role=\"{role}\">{escape(label)}</speaker>{nl}"
            f"{IND.L6}<u>{escape(utt)}</u>{nl}"
            f"{IND.L5}</div>"
        )

    xml = (
        f"{IND.TEXT}<text id=\"{doc_id}\">{nl}"
        f"{IND.L2}<meta>{nl}"
        f"{IND.L3}<Oral_History_Details>{nl}"
        f"{IND.L4}<Documents_ID>{doc_id}</Documents_ID>{nl}"
        f"{IND.L4}<Rec_Date>{field('Rec_Date')}</Rec_Date>{nl}"
        f"{IND.L4}<Rec_Length>{field('Length')}</Rec_Length>{nl}"
        f"{IND.L4}<A_Number>{field('A_#')}</A_Number>{nl}"
        f"{IND.L4}<Q_Number>{field('Q_#')}</Q_Number>{nl}"
        f"{IND.L4}<permission_type>{field('permission_type')}</permission_type>{nl}"
        f"{IND.L4}<Link>{field('Link')}</Link>{nl}"
        f"{IND.L3}</Oral_History_Details>{nl}"
        f"{IND.L3}<Individual_Meta_Data>{nl}"
        f"{IND.L4}<Name>{field('Name')}</Name>{nl}"
        f"{IND.L4}<DOB>{field('DOB')}</DOB>{nl}"
        f"{IND.L4}<Gender>{field('Gender')}</Gender>{nl}"
        f"{IND.L4}<Born>{field('Born')}</Born>{nl}"
        f"{IND.L4}<Ghetto>{field('Ghetto')}</Ghetto>{nl}"
        f"{IND.L4}<Camp>{field('Camp')}</Camp>{nl}"
        f"{IND.L4}<Imm_Date>{field('Imm_Date')}</Imm_Date>{nl}"
        f"{IND.L4}<Imm_Destination>{field('Imm_Destination')}</Imm_Destination>{nl}"
        f"{IND.L3}</Individual_Meta_Data>{nl}"
        f"{IND.L2}</meta>{nl}"
        f"{IND.L2}<text>{nl}"
        f"{IND.L3}<body>{nl}"
        f"{IND.L4}<div type=\"interview\">{nl}"
        f"{IND.L5}<head>Interview Transcript</head>{nl}"
        + (f"{nl}".join(div_blocks) + (nl if div_blocks else ""))
        + f"{IND.L4}</div>{nl}"
        f"{IND.L3}</body>{nl}"
        f"{IND.L2}</text>{nl}"
        f"{IND.TEXT}</text>"
    )

    q_count = sum(1 for t in turns if t[0] == "question")
    a_count = sum(1 for t in turns if t[0] == "answer")
    return xml, q_count, a_count


def read_metadata(metadata_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(metadata_csv, sep=None, engine="python", dtype=str).fillna("")
    if "Documents ID" not in df.columns:
        raise KeyError("Metadata file must contain a 'Documents ID' column.")
    return df


def generate_corhoh_xml(metadata_csv: Path, texts_dir: Path, output_xml: Path) -> None:
    df = read_metadata(metadata_csv)

    records: List[str] = []
    total_q = 0
    total_a = 0

    missing_transcripts = 0

    for i, row in enumerate(df.to_dict(orient="records"), start=1):
        doc_id = str(row.get("Documents ID", "")).strip()
        txt_path = texts_dir / f"{doc_id}.txt"

        if not txt_path.exists():
            missing_transcripts += 1
            logging.warning("Missing transcript for Documents ID '%s' (%s)", doc_id, txt_path)
            transcript = ""
        else:
            transcript = smart_read(txt_path)

        rec_xml, q, a = build_record_xml(row, transcript, "\n")
        records.append(rec_xml)
        total_q += q
        total_a += a

        if i % 50 == 0:
            logging.info("Processed %d/%d records...", i, len(df))

    logging.info("Total questions: %d | Total answers: %d", total_q, total_a)
    if missing_transcripts:
        logging.warning("Missing transcripts: %d (records were still created with empty text)", missing_transcripts)

    tei = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<TEI xmlns=\"http://www.tei-c.org/ns/1.0\">\n"
        + fixed_header_block(total_q, total_a, "\n")
        + f"\n{IND.CORHOH}<CORHOH>\n"
        + ("\n".join(records) + "\n")
        + f"{IND.CORHOH}</CORHOH>\n"
        + "</TEI>\n"
    )

    output_xml.write_text(tei, encoding="utf-8")
    logging.info("Wrote output: %s", output_xml)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate CORHOH TEI/XML file from metadata + transcripts")
    p.add_argument("--metadata", default=DEFAULT_METADATA_CSV, help="Path to metadata CSV")
    p.add_argument("--texts-dir", default=DEFAULT_TEXTS_DIR, help="Directory with transcript .txt files")
    p.add_argument("--output", default=DEFAULT_OUTPUT_XML, help="Output XML path")
    p.add_argument("-v", "--verbose", action="count", default=0, help="Increase logging (-v, -vv)")
    return p.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    metadata_csv = Path(args.metadata)
    texts_dir = Path(args.texts_dir)
    output_xml = Path(args.output)

    if not metadata_csv.exists():
        logging.error("Metadata file not found: %s", metadata_csv)
        return 2
    if not texts_dir.exists():
        logging.error("Texts directory not found: %s", texts_dir)
        return 2

    generate_corhoh_xml(metadata_csv, texts_dir, output_xml)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
