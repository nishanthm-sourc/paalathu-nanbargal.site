from pathlib import Path
import re
path = Path('ajith_anitha_wedding_v2.html')
text = path.read_text('utf-8')

name_to_url = {
    'Vicky': 'https://www.instagram.com/vikeerthi?igsh=MWk5dm1lZTR5amNuaA==',
    'Nishanth': 'https://www.instagram.com/mr_peradox?igsh=bTM5ZHE0OTN5Mm92',
    'Sridhar': 'https://www.instagram.com/sridharthomas0212?igsh=NWkya2dhcXpzaGd6',
    'Dhanasekaran': 'https://www.instagram.com/itz_dhana001?igsh=MXhxMHJzencza2RuaQ==',
    'Chinna': 'https://www.instagram.com/chinnappar_chinn?igsh=ZmNoazkwYjU3anJ0',
    'Ajay': 'https://www.instagram.com/ajayjustin_?igsh=MWJidGl2MmhkdWdjeA==',
    'Aswinth': 'https://www.instagram.com/its_aswinth?igsh=MWx1eHZsd3FmNmFzYg==',
    'Ajith Kumar': 'https://www.instagram.com/v.i.p_ponraj?igsh=MW80cW1zOG12NG92cg==',
}
pattern = re.compile(r'(<div class="poster-photo-wrap">.*?</div>)(\s*<div class="poster-top">.*?<p class="poster-name">([^<]+)</p>.*?</div>)', re.S)

count = 0


def wrap(m):
    global count
    block, rest, name = m.group(1), m.group(2), m.group(3).strip()
    url = name_to_url.get(name)
    if not url or '<a href="' in block:
        return m.group(0)
    wrapped = block.replace('<div class="poster-photo-wrap">', f'<div class="poster-photo-wrap"><a href="{url}" target="_blank" rel="noopener noreferrer" title="Visit {name} on Instagram">', 1)
    wrapped = wrapped.replace('</div>', '</a></div>', 1)
    count += 1
    return wrapped + rest

new_text = pattern.sub(wrap, text)
print('Inserted', count, 'Instagram links')
path.write_text(new_text, 'utf-8')
