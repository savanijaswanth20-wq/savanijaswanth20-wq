// Render the exported Higgsfield GLB with Three.js and headless Chromium.
// Requirements: npm install three@0.180.0 playwright
// Put scene.glb in the current directory, then run this script.
const fs=require('fs'), http=require('http'), path=require('path');
let chromium;
try { ({chromium}=require('playwright')); }
catch { ({chromium}=require('/usr/local/lib/node_modules/playwright')); }
const root=process.cwd();
const html=`<!doctype html><html><head><style>body{margin:0;background:#090f1e}canvas{display:block}</style><script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js","three/addons/":"/node_modules/three/examples/jsm/"}}</script></head><body><script type="module">
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});
renderer.setSize(640,640);
renderer.setPixelRatio(1);
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.NeutralToneMapping;
renderer.toneMappingExposure=1;
renderer.shadowMap.enabled=false;
document.body.appendChild(renderer.domElement);
const loaded=await new GLTFLoader().loadAsync('/scene.glb');
const scene=new THREE.Scene();scene.background=new THREE.Color('#090f1e');
scene.add(loaded.scene);
scene.add(new THREE.HemisphereLight(0x91b6e4,0x101527,.7));
let meshes=0;
loaded.scene.traverse(o=>{if(o.isMesh){o.castShadow=false;o.receiveShadow=false;meshes++;}if(o.isLight)o.castShadow=false;});
// A soft studio contact shadow avoids hard point-light shadows in portable GLB.
function contactShadow(size,y,opacity){
 const canvas=document.createElement('canvas');canvas.width=256;canvas.height=256;
 const ctx=canvas.getContext('2d'),g=ctx.createRadialGradient(128,128,12,128,128,128);
 g.addColorStop(0,'rgba(0,0,8,1)');g.addColorStop(.55,'rgba(0,0,8,.55)');g.addColorStop(1,'rgba(0,0,8,0)');
 ctx.fillStyle=g;ctx.fillRect(0,0,256,256);
 const plane=new THREE.Mesh(new THREE.PlaneGeometry(size,size),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(canvas),transparent:true,opacity,depthWrite:false}));
 plane.rotation.x=-Math.PI/2;plane.position.y=y;scene.add(plane);
}
contactShadow(5,-.074,.6);contactShadow(2.6,.125,.28);
const camera=loaded.cameras[0];
if(!camera)throw Error('Exported delivery camera missing');
camera.updateProjectionMatrix();
const mixer=new THREE.AnimationMixer(loaded.scene);
loaded.animations.forEach(clip=>mixer.clipAction(clip).play());
// Stretch the original four-second animation into a calmer six-second loop.
window.draw=t=>{mixer.setTime(t/1.5);scene.updateMatrixWorld(true);renderer.render(scene,camera);};
window.draw(0);
window.sceneInfo={meshes,animations:loaded.animations.length,durations:loaded.animations.map(a=>a.duration)};
window.ready=true;
</script></body></html>`;
const server=http.createServer((req,res)=>{
  const pathname=new URL(req.url,'http://localhost').pathname;
  if(pathname==='/'){res.setHeader('Content-Type','text/html');return res.end(html);}
  const file=path.resolve(root,'.'+pathname);
  if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
  if(!fs.existsSync(file)){res.writeHead(404);return res.end();}
  res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.glb')?'model/gltf-binary':'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,args:['--no-sandbox','--enable-webgl','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const page=await browser.newPage({viewport:{width:640,height:640},deviceScaleFactor:1});
  page.on('pageerror',e=>console.error('Page:',e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.waitForFunction(()=>window.ready,null,{timeout:60000});
  const info=await page.evaluate(()=>window.sceneInfo);
  if(info.animations<3)throw Error('Expected multiple animation tracks');
  console.log(JSON.stringify(info));
  fs.mkdirSync('frames',{recursive:true});
  for(let i=0;i<120;i++){
    await page.evaluate(t=>window.draw(t),i/20);
    await page.screenshot({path:'frames/'+String(i).padStart(3,'0')+'.png'});
  }
  await page.evaluate(()=>window.draw(0));
  const first=await page.screenshot();
  await page.evaluate(()=>window.draw(6));
  const last=await page.screenshot();
  fs.writeFileSync('loop-check.json',JSON.stringify({frames:120,fps:20,duration:6,firstFrameEqualsLoopEnd:first.equals(last),...info},null,2));
  console.log(fs.readFileSync('loop-check.json','utf8'));
  await browser.close();server.close();
})().catch(e=>{console.error(e);server.close();process.exit(1)});
