#!/usr/bin/env node
// 

const mqtt = require("mqtt");
const fs = require("fs");
const argv = require("yargs") // eslint-disable-line
  .option('port', {
    alias: 'p',
    describe: 'network port to connect to. Defaults to 1883.',
    default: 1883
  })
  .option('host', {
    alias: 'h',
    describe: 'mqtt host to connect to. Defaults to localhost.',
    default: "localhost",
    type: "string"
  })
  .option('topic', {
    alias: 't',
    describe: 'mqtt topic to publish to.',
    type: "string"
  })
  .option('message', {
    alias: 'm',
    describe: "message payload to send.",
    type: "string"
  })
  .option('protocol-version', {
    alias: 'V',
    describe: "specify the version of the MQTT protocol to use when connecting.\n\
      Can be mqttv31 or mqttv311. Defaults to mqttv31.",
    choices: ['mqttv31', 'mqttv311'],
    default: 'mqttv31'
  })
  .option('id', {
    alias: 'i',
    describe: "id to use for this client. Defaults to mosquitto_pub_ appended with the process id.",
    default: 'mosquitto_pub_1',
    type: 'string'
  })
  .option('file', {
    alias: 'f',
    describe: "send the contents of a file as the message.",
    type: 'string'
  })
  .option('stdin-file', {
    alias: 's',
    describe: "read message from stdin, sending the entire input as a message.",
    type: 'boolean'
  })
  .option('qos', {
    alias: 'q',
    describe: "quality of service level to use for all messages. Defaults to 0.",
    type: 'number',
    choices: [0, 1, 2],
    default: 0
  })
  .option('keepalive', {
    alias: 'k',
    describe: "keep alive in seconds for this client. Defaults to 60.",
    type: 'number',
    default: 60
  })
  .option('retain', {
    alias: 'r',
    describe: "If retain is given, the message will be retained as a "
      + "\"last known good\" value on the broker. See mqtt(7) for more information.",
    type: 'boolean',
    default: false
  })
  .argv;
const port = argv.port;
const host = argv.host;
const topic = argv.topic;
var message = argv.message;
if (!message) {
	if (argv.file) {
		message = fs.readFileSync(argv.file);
	} else {
		message = "";
	}
}
const qos = argv.qos;
const shouldRetain = argv.retain;
console.log("argv = ", JSON.stringify(argv));
let client = mqtt.connect({host: host, port: port});
client.on('connect', function() {
	console.log(`Sending message "${message}" from topic ${topic}.`);
	client.publish(topic, message, {
		qos: qos,
		retain: shouldRetain
	});
	console.log("Sent.");
	process.exit();
});
client.on('error', function() {
	console.err('Connection refused.');
	process.exit();
});
client.on('close', function() {
	console.log("Connection closed.");
	process.exit();
})
