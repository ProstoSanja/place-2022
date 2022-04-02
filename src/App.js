import './App.css';
import Timer from './Timer';
import githubLogo from './icons/github.svg';
import redditLogo from './icons/reddit.svg';
import ethLogo from './icons/eth.svg';
import linkedinLogo from './icons/linkedin.svg';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <video poster="" id="bgvid" playsInline autoPlay muted loop>
          <source src="24_hours.mp4" type="video/mp4"/>
        </video>
        <div className='anti-overlay'>
          
        </div>
        <div className='overlay'>
          <p className={"title"}>Looking back at r/Place</p>

          <div>
            <p>The reddit community has been drawing on the canvas for:</p>
            <Timer/>
          </div>

          <div>
            <button onClick={() => {window.open("/24_hours.mp4", '_blank').focus();}} className="large-btn">Download latest video</button>
            <button onClick={() => {window.open("/latest.zip", '_blank').focus();}} className="large-btn">Download raw data</button>
          </div>

          <div className="social">
            <button onClick={() => {window.open("https://github.com/ProstoSanja", '_blank').focus();}}><img src={githubLogo}/></button>
            <button onClick={() => {window.open("https://www.reddit.com/user/prosto_sanja", '_blank').focus();}}><img src={redditLogo}/></button>
            <button onClick={() => {window.open("https://www.linkedin.com/in/prostosanja/", '_blank').focus();}}><img src={linkedinLogo}/></button>
            <button onClick={() => {navigator.clipboard.writeText("0xA9040A0858A9A0292b354456fBF0d54918C3d456"); alert("Copied to clipboard: 0xA9040A0858A9A0292b354456fBF0d54918C3d456");}}><img src={ethLogo}/></button>
          </div>

          <div>
            <p className="hidden">Everyone is free to use the raw data and videos as long as you credit u/prosto_sanja or above linked github account</p>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
