import fs from 'node:fs';
import path from 'node:path';
const dir='docs/news';
const html=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function field(src,key) {
  const fm=src.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if(!fm)return '';
  const line=fm[1].split(/\r?\n/).find(x=>x.startsWith(key+':'));
  return line?line.slice(key.length+1).trim().replace(/^["']|["']$/g,''):'';
}
const news=fs.readdirSync(dir).filter(f=>f.endsWith('.md')&&f!=='index.md').map(f=>{
  const src=fs.readFileSync(path.join(dir,f),'utf8');
  const title=field(src,'title')||src.match(/^# (.+)$/m)?.[1];
  const date=field(src,'date');
  const m=date.match(/(\d{4})\s*年\s*(\d+)\s*月\s*(\d+)\s*日/)||date.match(/(\d{4})-(\d+)-(\d+)/);
  if(!title||!m){console.warn('Skipped:',f);return null}
  return {slug:f.slice(0,-3),title,date:m[1]+'年'+(+m[2])+'月'+(+m[3])+'日',key:(+m[1])*10000+(+m[2])*100+(+m[3])};
}).filter(Boolean).sort((a,b)=>b.key-a.key||a.slug.localeCompare(b.slug));
if(!news.length)throw Error('No articles');
let home=fs.readFileSync('docs/index.md','utf8');
const homePat=/(<div class="news-home__list">)[\s\S]*?(<\/div>)/;
if(!homePat.test(home))throw Error('News block missing on homepage');
const lines=news.slice(0,5).map(x=>'    <a class="news-home__item" href="/news/'+encodeURIComponent(x.slug)+'">\n      <span class="news-home__date">'+x.date+'</span>\n      <span class="news-home__title">'+html(x.title)+'</span>\n    </a>').join('\n');
home=home.replace(homePat,(_whole,opening,closing)=>opening+'\n'+lines+'\n  '+closing);
fs.writeFileSync('docs/index.md',home);
let index=fs.readFileSync('docs/news/index.md','utf8');
const indexPat=/<ul>[\s\S]*?<\/ul>/;
if(!indexPat.test(index))throw Error('News index missing');
const links=news.map(x=>'<li class="news-item"><a href="'+encodeURIComponent(x.slug)+'"><span class="news-title">'+html(x.title)+'</span><span class="news-date">'+x.date+'</span></a></li>').join('\n');
index=index.replace(indexPat,'<ul>\n'+links+'\n</ul>');
fs.writeFileSync('docs/news/index.md',index);
console.log('Generated homepage and news index:',news.length,'articles');
