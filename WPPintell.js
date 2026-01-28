const net = require("net");
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const BACKENDS = [
  { host: "127.0.0.1", port: 5050 },
  { host: "127.0.0.1", port: 5051 },
  { host: "127.0.0.1", port: 5052 },
  { host: "127.0.0.1", port: 5053 }
];

// intenta conectar a un backend
function sendToBackend(msgData, backend) {
  return new Promise((resolve, reject) => {
    const client = new net.Socket();
    let buffer = "";

    client.connect(backend.port, backend.host, () => {
      client.write(JSON.stringify(msgData) + "\n");
    });

    client.on("data", (data) => {
      buffer += data.toString();

      // procesar mensajes separados por \n
      let parts = buffer.split("\n");
      buffer = parts.pop(); // último fragmento incompleto

      for (let line of parts) {
        if (!line.trim()) continue;
        try {
          const res = JSON.parse(line.trim());

            console.log(`⏳ Backend ${backend.port} aceptó, procesando...`);
            client.destroy(); // cerrar después de respuesta final
            resolve(res);
          
        } catch (err) {
          console.error("⚠️ Error parseando JSON:", err);
        }
      }
    });

    client.on("error", (err) => {
      reject(err);
    });

    client.on("close", () => {
      if (buffer.trim()) {
        try {
          const res = JSON.parse(buffer.trim());
          resolve(res);
        } catch (err) {
          reject(err);
        }
      }
    });
  });
}

async function tryBackends(msgData) {
  for (const backend of BACKENDS) {
    try {
      const res = await sendToBackend(msgData, backend);
      console.log("✅ Backend OK:", backend.host + ":" + backend.port);

      // ejemplo de personalización tipo "Darcy"

      if (backend.port === 5050) {
        res.reply = "TST: " + res.reply;
      }
      if (backend.port === 5051) {
        res.reply = "DRC: " + res.reply;
      }
      if (backend.port === 5052) {
        res.reply = "ECO: " + res.reply;
      }
      if (backend.port === 5053) {
        res.reply = "AIR: " + res.reply;
      }

      return res;
    } catch (err) {
      console.warn("❌ Backend falló:", backend.host + ":" + backend.port, err.message);
    }
  }
  throw new Error("Todos los backends están offline");
}


// Inicia WhatsApp con sesión guardada
const client = new Client({
  authStrategy: new LocalAuth()
});

client.on("qr", qr => {
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("WhatsApp !READY!");
});

client.on("message", async msg => {
  if (msg.fromMe || msg.type !== "chat" || !msg.body) return;

  console.log("FROM:", msg.from,"MSG:", msg.body);

  try {
    const response = await tryBackends({
      from: msg.from,
      body: msg.body
    });

    if (response.reply) {
      await client.sendMessage(msg.from, response.reply);
      console.log("FP4W", msg.from, ":", response.data.reply,);
    }
  } catch (err) {
    console.error("Error TCP:", err.message);
    await client.sendMessage(msg.from, "😴 AI offline 😴");
  }
});

client.initialize();
