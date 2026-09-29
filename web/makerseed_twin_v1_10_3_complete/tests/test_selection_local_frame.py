from pathlib import Path
html = Path(__file__).resolve().parents[1] / 'standalone.html'
s = html.read_text(encoding='utf-8')
assert 'new T.BoxHelper' not in s, 'selection still uses world-axis-aligned BoxHelper'
assert 'function attachSelection' in s, 'local selection attach helper missing'
assert 'module.add(selection)' in s, 'selection is not parented to selected module'
assert 'computeLocalBounds' in s, 'local bounds computation missing'
print('PASS: selection outline uses module-local oriented bounds')
