// Higgsfield native compositor. Place the rendered core loop beside this file.
export default async ({ project }) => {
  const root = process.cwd();
  const p = await project({dir: './banner-project',size:'1100x540',fps:20,background:'#090f1e'});
  const core = await p.add(`${root}/core.mp4`);
  p.compose(
    <frame x={0} y={0} width={1100} height={540} layout="none">
      <rect x={0} y={0} width={1100} height={540} radius={28} fill="#090f1e" />
      <rect x={38} y={32} width={1024} height={1} fill="#28334d" />
      <text x={42} y={47} width={600} height={25} fontFamily="Montserrat" fontSize={12} fontWeight={600} letterSpacing={3} color="#b3c5df">SAVVANI VENKATA / DEVELOPER</text>
      <rect x={42} y={110} width={333} height={29} radius={14} fill="#142935" strokeColor="#2c5465" strokeWidth={1}/>
      <rect x={55} y={120} width={7} height={7} radius={4} fill="#79dfff" />
      <text x={73} y={117} width={296} height={20} fontFamily="Montserrat" fontSize={10} fontWeight={600} letterSpacing={1.2} color="#c5efff">PYTHON BACKEND &amp; AI DEVELOPER</text>
      <text x={38} y={156} width={590} height={105} fontFamily="Montserrat" fontSize={77} fontWeight={800} letterSpacing={-3} color="#f5f8ff">JASWANTH.</text>
      <text x={43} y={279} width={560} height={38} fontFamily="Montserrat" fontSize={26} fontWeight={500} color="#79dfff">Ideas into working products.</text>
      <text x={43} y={338} width={520} height={27} fontFamily="Montserrat" fontSize={17} fontWeight={400} color="#aebbd1">Python APIs. Practical AI integration.</text>
      <text x={43} y={367} width={520} height={27} fontFamily="Montserrat" fontSize={17} fontWeight={400} color="#aebbd1">Business applications built with purpose.</text>
      <rect x={42} y={424} width={550} height={1} fill="#28334d" />
      <text x={43} y={448} width={560} height={28} fontFamily="Montserrat" fontSize={12} fontWeight={500} letterSpacing={1.4} color="#b7c6dd">FASTAPI   /   SQL   /   REACT   /   RAG</text>
      <frame x={626} y={80} width={435} height={435} layout="none" radius={26} clip={true}>
        <media x={0} y={0} file={core} width={435} height={435} fit="cover" />
      </frame>
      <text x={704} y={48} width={356} height={24} fontFamily="Montserrat" fontSize={10} fontWeight={500} letterSpacing={2.3} color="#91a0bb">01 / BUILD · CONNECT · IMPROVE</text>
      <rect x={42} y={506} width={1020} height={1} fill="#28334d" />
    </frame>,
    {dur:6,name:'Jaswanth 3D profile banner'}
  );
  await p.frame(1,`${root}/hero.png`);
  await p.render(`${root}/hero.mp4`,{bitrate:5000000,accel:'cpu'});

  const m = await project({dir:'./mobile-project',size:'640x850',fps:20,background:'#090f1e'});
  const mobileCore=await m.add(`${root}/core.mp4`);
  m.compose(
    <frame x={0} y={0} width={640} height={850} layout="none">
      <rect x={0} y={0} width={640} height={850} fill="#090f1e"/>
      <text x={30} y={32} width={580} height={26} fontFamily="Montserrat" fontSize={13} fontWeight={600} letterSpacing={2} color="#b3c5df">SAVVANI VENKATA / DEVELOPER</text>
      <text x={25} y={81} width={595} height={100} fontFamily="Montserrat" fontSize={78} fontWeight={800} letterSpacing={-3} color="#f5f8ff">JASWANTH.</text>
      <text x={30} y={196} width={580} height={39} fontFamily="Montserrat" fontSize={24} fontWeight={500} color="#79dfff">Ideas into working products.</text>
      <text x={30} y={248} width={580} height={30} fontFamily="Montserrat" fontSize={19} fontWeight={500} color="#aebbd1">Python Backend &amp; AI Developer</text>
      <frame x={50} y={290} width={540} height={500} layout="none" clip={true} radius={26}>
        <media x={0} y={0} file={mobileCore} width={540} height={540} fit="cover"/>
      </frame>
      <text x={30} y={807} width={580} height={25} fontFamily="Montserrat" fontSize={13} fontWeight={500} letterSpacing={1.3} color="#b7c6dd">FASTAPI   /   SQL   /   REACT   /   RAG</text>
    </frame>,{dur:6,name:'Mobile 3D profile banner'}
  );
  await m.frame(1,`${root}/hero-mobile.png`);
  await m.render(`${root}/hero-mobile.mp4`,{bitrate:5000000,accel:'cpu'});
};
