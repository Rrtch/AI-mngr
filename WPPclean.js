const net = require("net");
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const PYTHON_PORT = 5050;
const PYTHON_HOST = "127.0.0.1";

function sendToPython(msgData) {
  return new Promise((resolve, reject) => {
    const client = new net.Socket();

    client.connect(PYTHON_PORT, PYTHON_HOST, () => {
      client.write(JSON.stringify(msgData));
    });

    client.on("data", (data) => {
      try {
        const res = JSON.parse(data.toString());
        client.destroy();
        resolve(res);
      } catch (err) {
        reject(err);
      }
    });

    client.on("error", (err) => {
      reject(err);
    });
  });
}

// Inicia WhatsApp con sesión guardada
const client = new Client({
  authStrategy: new LocalAuth()
});

client.on("qr", qr => {
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("WhatsApp READY!");
});

client.on("message", async msg => {
  if (msg.fromMe || msg.type !== "chat" || !msg.body) return;

  console.log("FROM:", msg.from, "MSG:", msg.body);

  try {
    const response = await sendToPython({
      from: msg.from,
      body: msg.body
    });

    if (response.reply) {
      await client.sendMessage(msg.from, response.reply);
      console.log("FP4W:", msg.from, ":", response.reply);
    }
  } catch (err) {
    console.error("Error TCP:", err.message);
    await client.sendMessage(msg.from, "😴 AI offline 😴");
  }
});

client.initialize();
