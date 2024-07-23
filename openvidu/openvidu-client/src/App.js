import React, { useState, useRef } from 'react';
import { OpenVidu } from 'openvidu-browser';

const OPENVIDU_SERVER_URL = 'https://143.248.199.16:4443';
const OPENVIDU_SERVER_SECRET = '1234';

function App() {
  const [mySessionId, setMySessionId] = useState('SessionA');
  const [myUserName, setMyUserName] = useState('Participant' + Math.floor(Math.random() * 100));
  const [session, setSession] = useState(null);
  const [mainStreamManager, setMainStreamManager] = useState(null);
  const [publisher, setPublisher] = useState(null);
  const [subscribers, setSubscribers] = useState([]);
  const sessionRef = useRef(null);

  const joinSession = async () => {
    const openvidu = new OpenVidu();
    openvidu.setAdvancedConfiguration({
      websocketUrl: OPENVIDU_SERVER_URL,
      secret: OPENVIDU_SERVER_SECRET
    });
    const session = openvidu.initSession();

    session.on('streamCreated', (event) => {
      const subscriber = session.subscribe(event.stream, undefined);
      setSubscribers(prevSubscribers => [...prevSubscribers, subscriber]);
    });

    sessionRef.current = session;

    try {
      const response = await fetch('https://143.248.199.16:5001/api/sessions', {
        method: 'POST'
      });
      const sessionId = await response.text();

      const tokenResponse = await fetch(`https://143.248.199.16:5001/api/sessions/${sessionId}/connections`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userName: myUserName })
      });
      const token = await tokenResponse.text();

      await session.connect(token, { clientData: myUserName });

      const publisher = openvidu.initPublisher(undefined, {
        audioSource: undefined,
        videoSource: undefined,
        publishAudio: true,
        publishVideo: true,
        resolution: '640x480',
        frameRate: 30,
        insertMode: 'APPEND',
        mirror: false
      });

      session.publish(publisher);

      setSession(session);
      setMainStreamManager(publisher);
      setPublisher(publisher);
    } catch (error) {
      console.error('Error connecting to session:', error);
    }
  };

  const leaveSession = () => {
    if (session) {
      session.disconnect();
    }

    setSession(null);
    setMainStreamManager(null);
    setPublisher(null);
    setSubscribers([]);
  };

  return (
    <div className="App">
      <div>
        <h1>OpenVidu React App</h1>
        {session === null ? (
          <div>
            <input
              type="text"
              value={mySessionId}
              onChange={(e) => setMySessionId(e.target.value)}
              placeholder="Session ID"
            />
            <input
              type="text"
              value={myUserName}
              onChange={(e) => setMyUserName(e.target.value)}
              placeholder="User Name"
            />
            <button onClick={joinSession}>Join</button>
          </div>
        ) : (
          <button onClick={leaveSession}>Leave session</button>
        )}
      </div>

      {mainStreamManager !== null && (
        <div id="video-container">
          <div>
            <h2>{myUserName}</h2>
            <div id="publisher" ref={(node) => node && mainStreamManager.addVideoElement(node)}></div>
          </div>
          {subscribers.map((sub, index) => (
            <div key={index}>
              <h2>Subscriber</h2>
              <div ref={(node) => node && sub.addVideoElement(node)}></div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
