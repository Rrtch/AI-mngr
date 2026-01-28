const net = require("net");
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const PYTHON_PORT = 5050;
const PYTHON_HOST = "127.0.0.1";
const GRE = "\x1b[32m";
const RES = "\x1b[0m";
const DRK_GRE  = "\x1b[38;5;22m"

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
  console.log(DRK_GRE+"WhatsApp "+RES+"¡READY!");
});

// Guarda la marca de tiempo del último mensaje
let lastMessageTs = Date.now();

// Cuando llega un mensaje
client.on("message", async msg => {
  lastMessageTs = Date.now(); // actualiza el timestamp
  if (msg.fromMe) return;
  if (msg.fromMe || msg.type !== "chat" || !msg.body) return;

  console.log(GRE+"FROM:"+DRK_GRE, msg.from,GRE+"MSG:"+DRK_GRE, msg.body,RES);

  // ignorar mensajes de status@broadcast
  if (msg.from === "status@broadcast") {
    console.log("⚠️ Ignorado mensaje de status@broadcast");
    return; // se sale sin procesar
  }

  try {
    const response = await sendToPython({
      from: msg.from,
      body: msg.body
    });

    if (response.reply) {
      await client.sendMessage(msg.from, response.reply);
      console.log(GRE+"FP4W:"+RES, msg.from, ":", response.reply);
    }
  } catch (err) {
    console.error("Error TCP:", err.message);
    await client.sendMessage(msg.from, "😴 AI offline 😴");
  }
});

// Watchdog: revisa cada 5 minutos
setInterval(async () => {
  const diff = Date.now() - lastMessageTs;
  const maxSilent = 1000 * 60 * 30; // 10 minutos

  if (diff > maxSilent) {
    console.warn("⚠️ 10 minutos sin mensajes, reiniciando cliente...");
    try {
      await client.destroy();
    } catch (e) {
      console.error("Error al destruir cliente:", e.message);
    }
    client.initialize(); // vuelve a conectar
    lastMessageTs = Date.now(); // reinicia el contador
  }
}, 1000 * 60 * 5); // cada 5 minutos

client.initialize();

// Endpoint HTTP para enviar mensajes desde Python

client.on("disconnected", reason => {
  console.error("Cliente desconectado:", reason);
  client.initialize(); // reconecta automático
});

client.on("auth_failure", msg => {
  console.error("Error de autenticación:", msg);
  // Aquí normalmente toca borrar el LocalAuth y reescanear QR
});