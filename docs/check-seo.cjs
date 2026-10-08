/* Run with the bundled Node runtime and NODE_PATH pointing to bundled packages. */
const { chromium } = require('playwright');
const fs = require('node:fs');
(async () => {
 const browser = await chromium.launch({headless:true, executablePath:'/usr/bin/google-chrome', args:['--no-sandbox']});
 const page = await browser.newPage();
 const routes = ['', 'zaciname', 'co-koupit', 'navody', 'pomoc', 'novinky', 'ai', 'zigbee', 'integrace', 'automatizace', 'o-projektu', 'zaciname/instalace-home-assistant', 'zigbee/zha-vs-zigbee2mqtt'];
 const results = [];
 for (const width of [360,390,768,1440]) {
  await page.setViewportSize({width,height:900});
  for (const route of routes) {
   const response=await page.goto(`http://127.0.0.1:8765/${route}${route?'/':''}`);
   const data=await page.evaluate(()=>({
    title:document.title,h1:[...document.querySelectorAll('h1')].map(x=>x.textContent),
    canonical:document.querySelector('link[rel=canonical]')?.href,
    description:document.querySelector('meta[name=description]')?.content,
    overflow:document.documentElement.scrollWidth>innerWidth,
    schema:[...document.querySelectorAll('script[type="application/ld+json"]')].map(x=>JSON.parse(x.textContent)),
    brokenImages:[...document.images].filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.src)
   }));
   if(response.status()!==200||data.h1.length!==1||data.canonical!==`https://www.hawiki.cz/${route}${route?'/':''}`||!data.description||data.overflow||data.brokenImages.length) throw Error(JSON.stringify({route,width,status:response.status(),...data}));
   results.push({route:'/'+route+(route?'/':''),width,status:response.status(),title:data.title,h1:data.h1[0],canonical:data.canonical,description:data.description,overflow:data.overflow});
  }
 }
 for(const [route,width] of [['',1440],['',390],['zigbee',360],['zaciname',768],['zigbee/zha-vs-zigbee2mqtt',390]]) {
  await page.setViewportSize({width,height:900}); await page.goto('http://127.0.0.1:8765/'+route+(route?'/':''));
  await page.screenshot({path:`/tmp/hawiki-${route.replaceAll('/','-')||'home'}-${width}.png`,fullPage:true});
 }
 fs.writeFileSync('seo-preview/docs/seo-validation.json',JSON.stringify(results,null,2));
 await browser.close(); console.log(`Passed ${results.length} HTTP/metadata/mobile checks.`);
})().catch(e=>{console.error(e);process.exit(1)});
