const fs = require('fs');
const net = require('net');
const socketPath = '/tmp/socket_file';

const client = net.createConnection({ path: socketPath}, () => {
    console.log('connect to server');

    fs.readFile('rpc_json/reverse.json', (err, data) => {
        if (err) throw err;

        client.write(data);
        client.end();
    })
});

client.on('data', (data) => {
    console.log(data.toString());
});

client.on('end', () => {
    console.log('disconnected from server');
});
