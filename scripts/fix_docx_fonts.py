"""Post-process pandoc-generated docx to apply SimSun + Times New Roman fonts,
1.5x line spacing, justified alignment, and heading sizes.

Usage: python fix_docx_fonts.py <input.docx> [output.docx]
If output is omitted, modifies input in-place.
"""

import zipfile, os, shutil, re, sys, tempfile

def fix_docx(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    # Use an absolute temp directory to avoid CWD-dependence and
    # Chinese-path encoding issues on Windows
    extract_dir = os.path.join(tempfile.gettempdir(), "_docx_fix_temp")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    try:
        with zipfile.ZipFile(input_path, "r") as z:
            z.extractall(extract_dir)

        # --- styles.xml ---
        styles_path = os.path.join(extract_dir, "word", "styles.xml")
        if not os.path.exists(styles_path):
            raise FileNotFoundError(f"styles.xml not found in {input_path}")

        with open(styles_path, "r", encoding="utf-8") as f:
            xml = f.read()

        # docDefaults - rPr (fonts + body size)
        xml = xml.replace(
            "<w:rPrDefault>",
            '<w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="SimSun" w:cs="Times New Roman"/><w:sz w:val="24"/></w:rPr>'
        )

        # docDefaults - pPr (justified + 1.5 spacing)
        xml = xml.replace(
            "<w:pPrDefault>",
            '<w:pPrDefault><w:pPr><w:jc w:val="both"/><w:spacing w:line="360" w:lineRule="auto"/></w:pPr>'
        )

        # Normal style
        xml = xml.replace(
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">',
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:pPr><w:jc w:val="both"/><w:spacing w:line="360" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="SimSun" w:cs="Times New Roman"/><w:sz w:val="24"/></w:rPr>'
        )

        # Heading 1 (22pt bold)
        xml = re.sub(
            r'(<w:style w:type="paragraph" w:styleId="Heading1">.*?</w:pPr>)<w:rPr>.*?</w:rPr>',
            r'\1<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="SimSun" w:cs="Times New Roman"/><w:b/><w:sz w:val="44"/><w:szCs w:val="44"/></w:rPr>',
            xml, flags=re.DOTALL
        )

        # Heading 2 (16pt bold)
        xml = re.sub(
            r'(<w:style w:type="paragraph" w:styleId="Heading2">.*?</w:pPr>)<w:rPr>.*?</w:rPr>',
            r'\1<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="SimSun" w:cs="Times New Roman"/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>',
            xml, flags=re.DOTALL
        )

        # Heading 3 (14pt bold)
        xml = re.sub(
            r'(<w:style w:type="paragraph" w:styleId="Heading3">.*?</w:pPr>)<w:rPr>.*?</w:rPr>',
            r'\1<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="SimSun" w:cs="Times New Roman"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>',
            xml, flags=re.DOTALL
        )

        with open(styles_path, "w", encoding="utf-8") as f:
            f.write(xml)

        # --- theme1.xml ---
        theme_path = os.path.join(extract_dir, "word", "theme", "theme1.xml")
        if os.path.exists(theme_path):
            with open(theme_path, "r", encoding="utf-8") as f:
                txml = f.read()

            txml = re.sub(
                r"<a:majorFont>.*?</a:majorFont>",
                '<a:majorFont><a:latin typeface="Times New Roman"/><a:ea typeface="SimSun"/><a:cs typeface="Times New Roman"/></a:majorFont>',
                txml, flags=re.DOTALL
            )

            txml = re.sub(
                r"<a:minorFont>.*?</a:minorFont>",
                '<a:minorFont><a:latin typeface="Times New Roman"/><a:ea typeface="SimSun"/><a:cs typeface="Times New Roman"/></a:minorFont>',
                txml, flags=re.DOTALL
            )

            with open(theme_path, "w", encoding="utf-8") as f:
                f.write(txml)

        # --- Repack ---
        # Write to a temp file first, then replace original
        tmp_output = output_path + ".tmp"
        with zipfile.ZipFile(tmp_output, "w", zipfile.ZIP_DEFLATED) as zout:
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    full = os.path.join(root, file)
                    arcname = os.path.relpath(full, extract_dir)
                    zout.write(full, arcname)

        # Atomic replace on Windows
        if os.path.exists(output_path):
            os.remove(output_path)
        os.rename(tmp_output, output_path)

    finally:
        shutil.rmtree(extract_dir, ignore_errors=True)

    print(f"Fixed: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_docx_fonts.py <input.docx> [output.docx]")
        sys.exit(1)
    input_path = os.path.abspath(sys.argv[1])
    output_path = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None
    fix_docx(input_path, output_path)
