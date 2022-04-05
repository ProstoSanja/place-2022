import './App.css';
import Timer from './Timer';
import githubLogo from './icons/github.svg';
import redditLogo from './icons/reddit.svg';
import ethLogo from './icons/eth.svg';
import linkedinLogo from './icons/linkedin.svg';
import { useCallback, useEffect, useState } from 'react';

function App() {

  const [visible, setVisible] = useState(false);
  const escFunction = useCallback((event) => {
    if (event.key === "Escape") {
      setVisible(false)
    }
  }, []);

  useEffect(() => {
    document.addEventListener("keydown", escFunction, false);

    return () => {
      document.removeEventListener("keydown", escFunction, false);
    };
  }, [escFunction]);

  return (
    <div className="App">
      <header className="App-header">
        <video poster="" id="bgvid" playsInline autoPlay muted loop>
          <source src="preview.webm" type="video/webm"/>
        </video>
        <div className='anti-overlay'>
          
        </div>
        <div className='overlay'>
          <p className={"title"}>Looking back at r/Place</p>

          <div>
            <p>The reddit community has been drawing on the canvas for:</p>
            <p>3 days and 12 hours</p>
          </div>

          <div className="button-holder">
            <button onClick={() => {window.open("https://youtu.be/29giASnhAa8", '_blank').focus();}} className="large-btn">Latest video</button>
            <button onClick={() => {window.open("/final_v1.zip", '_blank').focus();}} className="large-btn">Download raw data (final v1)</button>
            <button onClick={() => setVisible(true)} className="large-btn">Projects by others</button>
          </div>

          <div className="social">
            <button onClick={() => {window.open("https://github.com/ProstoSanja/place-2022", '_blank').focus();}}><img alt="github link" src={githubLogo}/></button>
            <button onClick={() => {window.open("https://www.reddit.com/user/prosto_sanja", '_blank').focus();}}><img alt="reddit link" src={redditLogo}/></button>
            <button onClick={() => {window.open("https://www.linkedin.com/in/prostosanja/", '_blank').focus();}}><img alt="linkedin link" src={linkedinLogo}/></button>
            <button onClick={() => {navigator.clipboard.writeText("0xA9040A0858A9A0292b354456fBF0d54918C3d456"); alert("Copied to clipboard: 0xA9040A0858A9A0292b354456fBF0d54918C3d456");}}><img alt="ethereum link" src={ethLogo}/></button>
          </div>

          <div>
            <p className="hidden">Everyone is free to use the raw data and videos as long as you credit u/prosto_sanja or above linked github account</p>
          </div>
        </div>
      </header>
        
      <div className={visible ? "popup visible" : "popup"}  onClick={(e) => e.target.classList.contains("popup") ? setVisible(false) : null} >
        <div className="popup_inner">
          
          <p className={"title"}>Projects by other people</p>
          <button onClick={() => {window.open("https://place-atlas.stefanocoding.me/", '_blank').focus();}} className="large-btn">r/Place atlas by Stefano Haagmans</button>
          <button onClick={() => {window.open("/heatmap_36h.mp4", '_blank').focus();}} className="large-btn">r/Place heatmap by u/DeathByElectives</button>
          <button onClick={() => {window.open("https://www.youtube.com/watch?v=jO1st_gpk50", '_blank').focus();}} className="large-btn">r/Place delta heatmap by u/Nuyube</button>
          <button onClick={() => {window.open("https://rplace.space/", '_blank').focus();}} className="large-btn">r/Place constantly updating timelapse by u/risson67</button>
          <p>Parts of missing data provided by u/moody_puffin</p>
          <button onClick={() => {setVisible(false)}} className="large-btn">Close</button>
        </div>
      </div>
    </div>
  );
}

export default App;
