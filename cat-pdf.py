import fitz
from sys import argv

if i := argv.index("-o"):
    _ = argv.pop(i)
    output = argv.pop(i)  # Assume `-o output.pdf`
else:
    output = "output.pdf"


def page_plus(offset):
    def page_plus_offset(row):
        row[2] += offset
        return row

    return page_plus_offset


with fitz.open() as doc:
    toc = []
    for chapter in argv[1:]:
        with fitz.open(chapter) as f:
            # Ignore t[3] (get_toc(False)) in case kind == fitz.LINK_NAMED
            toc.extend(map(page_plus(len(doc)), f.get_toc()))

            # Metadata is unchanged, that's why we need to manually set toc
            doc.insert_pdf(f)

    doc.set_toc(toc)
    doc.save(output, garbage=3, deflate=True)
