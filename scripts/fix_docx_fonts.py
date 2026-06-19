"""Post-process pandoc-generated docx to apply SimSun + Times New Roman fonts,
1.5x line spacing, justified alignment, and heading sizes."""

import zipfile, os, shutil, re, sys

def fix_docx(input_path, output_path):
    extract_dir = os.path.join(os.path.dirname(input_path), "_docx_temp_extract")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)

    # Copy to output first (so we modify a copy)
    if input_path != output_path:
        shutil.copy2(input_path, output_path)

    with zipfile.ZipFile(output_path, "r") as z:
        z.extractall(extract_dir)

    # --- styles.xml ---
    styles_path = os.path.join(extract_dir, "word", "styles.xml")
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
    os.remove(output_path)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                full = os.path.join(root, file)
                arcname = os.path.relpath(full, extract_dir)
                zout.write(full, arcname)

    shutil.rmtree(extract_dir)
    print(f"Fixed: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fix_docx_fonts.py <input.docx> <output.docx>")
        sys.exit(1)
    fix_docx(sys.argv[1], sys.argv[2])
