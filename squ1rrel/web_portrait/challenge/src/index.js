const express = require("express");
const { MongoClient } = require("mongodb");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");

const JWT_SECRET = process.env.JWT_SECRET; // Change this to a more secure value
const JWT_EXPIRATION = "1h"; // Token expiration time

const app = express();
app.use(express.json());

const url = process.env.ME_CONFIG_MONGODB_URL || "mongodb://localhost:27017";
const client = new MongoClient(url);
let db;

async function start() {
  await client.connect();
  db = client.db("ctf_challenge");
  console.log("Database initialized");
}

// Middleware to verify JWT token
function authenticate(req, res, next) {
  const token = req.headers["authorization"]?.replace("Bearer ", "");
  if (!token) {
    return res.status(401).json({ message: "Missing token" });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ message: "Invalid token" });
  }
}

app.post("/api/register", async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ message: "Missing username or password" });
  }

  if (username.length < 6) {
    return res
      .status(400)
      .json({ message: "Username must be at least 6 characters" });
  }

  const existing = await db.collection("accounts").findOne({ username });
  if (existing) {
    return res.status(400).json({ message: "Username already exists" });
  }

  const hashedPassword = await bcrypt.hash(password, 10);
  await db
    .collection("accounts")
    .insertOne({ username, password: hashedPassword, balance: BigInt(0) });
  const token = jwt.sign({ username }, JWT_SECRET, {
    expiresIn: JWT_EXPIRATION,
  });
  res.json({ token });
});

app.post("/api/login", async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ message: "Missing username or password" });
  }

  const account = await db.collection("accounts").findOne({ username });
  if (!account) {
    return res.status(400).json({ message: "Invalid username or password" });
  }

  const isPasswordValid = await bcrypt.compare(password, account.password);
  if (!isPasswordValid) {
    return res.status(400).json({ message: "Invalid username or password" });
  }

  const token = jwt.sign({ username }, JWT_SECRET, {
    expiresIn: JWT_EXPIRATION,
  });
  res.json({ token });
});

app.post("/api/portraits", authenticate, async (req, res) => {
  const { username } = req.user;
  const { source, name } = req.body;

  if (!source) {
    return res.status(400).send("Missing portrait");
  }

  await db.collection("portraits").insertOne({ username, source, name });
  res.json({ message: "Portrait saved" });
});

app.get("/api/portraits/:username", async (req, res) => {
  const { username } = req.params;
  const portraits = await db
    .collection("portraits")
    .find({ username })
    .toArray();
  res.json(portraits);
});

app.get("/", (req, res) => {
  // send index.html
  res.sendFile(__dirname + "/static/index.html");
});

app.get("/gallery", (req, res) => {
  res.sendFile(__dirname + "/static/gallery.html");
});

app.get("/register", (req, res) => {
  res.sendFile(__dirname + "/static/register.html");
});

start().then(() =>
  app.listen(3000, () => console.log("Server running on http://localhost:3000"))
);
