const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})




app.get('/audio', (req, res) => {
  res.sendFile('./audio.html', { root: __dirname });
});


app.get('/*', (req, res) => {
  console.log(req.originalUrl);
  res.sendFile(req.originalUrl+'.html', { root: __dirname });
});


app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
