# SVG Manager - Quick Reference Guide

## 📋 Overview

This tool extracts SVG content from HTML files and restores them later, even if the HTML has been modified. It uses smart placeholders with context information to ensure SVGs return to their correct positions.

## 🚀 Quick Start

### 1. Extract SVGs from HTML
```bash
python svg_manager.py extract index.html --output svgs.json
```

**Output:**
- `svgs.json` - Contains all SVG data
- `index_with_placeholders.html` - HTML with placeholders instead of SVGs

### 2. Edit Your HTML
Now you can safely edit `index_with_placeholders.html`:
- Change text content
- Add or remove sections
- Modify structure
- The placeholders will preserve SVG positions

### 3. Restore SVGs
```bash
python svg_manager.py restore index_with_placeholders.html svgs.json --output final.html
```

**Output:**
- `final.html` - Complete HTML with SVGs back in place

## 📊 View Statistics
```bash
python svg_manager.py stats svgs.json
```

Shows:
- Total number of SVGs
- Size information
- Individual SVG details

## 🧪 Test the Tool
```bash
python test_svg_manager.py
```

Runs a complete test to verify extraction and restoration work correctly.

## 💡 Use Cases

### Scenario 1: Reduce File Size for Editing
SVGs make HTML files large and hard to edit. Extract them:
```bash
python svg_manager.py extract large_file.html
# Edit large_file_with_placeholders.html (much smaller!)
python svg_manager.py restore large_file_with_placeholders.html svgs.json -o final.html
```

### Scenario 2: Version Control
Extract SVGs before committing to git:
```bash
python svg_manager.py extract index.html
git add index_with_placeholders.html svgs.json
git commit -m "Separated SVGs for better diffing"
```

### Scenario 3: Content Translation
Translate text without worrying about SVG code:
```bash
python svg_manager.py extract page.html
# Translate page_with_placeholders.html
# Placeholders remain unchanged
python svg_manager.py restore page_with_placeholders.html svgs.json -o translated.html
```

### Scenario 4: Batch Processing
Process multiple files:
```bash
for file in *.html; do
    python svg_manager.py extract "$file" --output "${file%.html}_svgs.json"
done
```

## 🔧 Advanced Options

### Custom Context Length
Use more context for better placement (default is 150 characters):
```bash
python svg_manager.py extract index.html --context 300
```

### Custom Output Filenames
```bash
python svg_manager.py extract index.html \
    --output my_svgs.json \
    --html-output cleaned.html
```

## 📝 Placeholder Format

Placeholders look like this:
```html
<!-- SVG_PLACEHOLDER_START:0001_a3f2b8e9 -->
<!-- CONTEXT_BEFORE: ...surrounding text before... -->
<!-- CONTEXT_AFTER: ...surrounding text after... -->
<span class="svg-placeholder" data-svg-id="0001_a3f2b8e9"></span>
<!-- SVG_PLACEHOLDER_END:0001_a3f2b8e9 -->
```

## 🐍 Python API

Use in your own scripts:

```python
from svg_manager import SVGManager

# Create manager
manager = SVGManager(context_chars=150)

# Extract
with open('input.html', 'r') as f:
    html = f.read()
modified_html, svg_data = manager.extract_svgs(html)

# Save
manager.save_svg_data(svg_data, 'svgs.json')

# Later: Restore
svg_data = manager.load_svg_data('svgs.json')
restored = manager.restore_svgs(modified_html, svg_data)
```

## ✅ Verification

The tool ensures:
- ✓ All SVGs are extracted
- ✓ Unique IDs for each SVG
- ✓ Context preservation
- ✓ 100% restoration accuracy
- ✓ No data loss

## 🆘 Troubleshooting

**Problem:** SVGs not extracted
- **Solution:** Ensure SVG tags are properly closed with `</svg>`

**Problem:** Restoration incomplete
- **Solution:** Don't manually edit placeholder comments

**Problem:** Wrong placement after restoration
- **Solution:** Increase context length: `--context 300`

## 📁 Files Generated

| File | Description |
|------|-------------|
| `svgs.json` | SVG data and metadata |
| `*_with_placeholders.html` | HTML with placeholders |
| `*_restored.html` | Restored HTML with SVGs |

## 🎯 Best Practices

1. **Always backup** your original HTML before extraction
2. **Don't edit** placeholder comments manually
3. **Version control** both the JSON and HTML files together
4. **Test restoration** before using in production
5. **Use meaningful filenames** for clarity

## 📖 Full Documentation

See `README_SVG_MANAGER.md` for complete documentation.

## 🧩 Example Workflow

Complete example:
```bash
# 1. Test that it works
python test_svg_manager.py

# 2. Extract SVGs from your file
python svg_manager.py extract mypage.html

# 3. Check what was extracted
python svg_manager.py stats svgs.json

# 4. Edit the HTML (without SVGs)
nano mypage_with_placeholders.html

# 5. Restore SVGs
python svg_manager.py restore mypage_with_placeholders.html svgs.json -o final.html

# 6. Verify it worked
diff mypage.html final.html
```

## 💾 JSON Structure

The JSON file contains:
```json
{
  "metadata": {
    "extraction_date": "2025-10-15T12:00:00",
    "total_svgs": 43,
    "context_chars": 150
  },
  "svgs": [
    {
      "id": "0001_a3f2b8e9",
      "index": 0,
      "svg_content": "<svg>...</svg>",
      "context_before": "...",
      "context_after": "...",
      "original_position": {"start": 1234, "end": 5678}
    }
  ]
}
```

---

**Made with ❤️ for easier HTML editing**
