const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { OpenVidu } = require('openvidu-node-client');

const app = express();
app.use(cors());
app.use(bodyParser.json());

const OPENVIDU_URL = 'https://143.248.199.16:4443';
const OPENVIDU_SECRET = '1234';

const openvidu = new OpenVidu(OPENVIDU_URL, OPENVIDU_SECRET);

app.post('/api/sessions', async (req, res) => {
    try {
      const session = await openvidu.createSession();
      res.status(200).send(session.sessionId);
    } catch (error) {
      console.error('Error creating session:', JSON.stringify(error, null, 2));
      res.status(500).send('Error creating session');
    }
  });
  
  app.post('/api/sessions/:sessionId/connections', async (req, res) => {
    const sessionId = req.params.sessionId;
    const userData = req.body.userName; // 클라이언트에서 전송한 사용자 이름
    try {
      const connection = await openvidu.createConnection(sessionId, { data: userData });
      res.status(200).send(connection.token);
    } catch (error) {
      console.error('Error creating connection:', JSON.stringify(error, null, 2));
      res.status(500).send('Error creating connection');
    }
  });
app.listen(5001, () => {
  console.log('Server started on port 5001');
});