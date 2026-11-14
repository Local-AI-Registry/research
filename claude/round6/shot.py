from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w,tag in [(1040,'d'),(390,'m')]:
        pg=b.new_page(viewport={'width':w,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file:///home/claude/work/r6/test3.html')
        if tag=='m': pg.add_style_tag(content='body{width:auto} article{width:auto!important;margin:6px!important;padding:12px!important}')
        for i,a in enumerate(pg.query_selector_all('article')):
            bb=a.query_selector('svg').bounding_box()
            pg.mouse.move(bb['x']+bb['width']*0.02,bb["y"]+bb["height"]*0.02)
            a.screenshot(path=f's_{tag}{i+11}.png')
        print(tag,errs)
    b.close()
