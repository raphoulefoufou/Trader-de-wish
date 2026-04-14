const express = require('express');
const cors = require('cors');
const YahooFinance = require('yahoo-finance2').default;
const { exec } = require('child_process');
const path = require('path');
const http = require('http');
const yahooFinance = new YahooFinance({ suppressNotices: ['ripHistorical'] });

const app = express();
app.use(cors());
const PORT = 3000;
const FLASK_PORT = 5000;

const htmlContent = `
<!DOCTYPE HTML>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Bourse Expert - IA Prédiction</title>
    <script src="https://cdn.canvasjs.com/canvasjs.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #0f0f0f; color: #e0e0e0; padding: 20px; text-align: center; }
        .menu { background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 20px; display: inline-flex; gap: 15px; align-items: center; border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); flex-wrap: wrap; justify-content: center; }
        select, button { padding: 10px; border-radius: 6px; border: 1px solid #444; background: #2a2a2a; color: white; cursor: pointer; outline: none; }
        button { background: #007bff; border: none; font-weight: bold; padding: 10px 25px; transition: 0.2s; }
        button:hover { background: #0056b3; transform: translateY(-2px); }
        h2 { color: #00d4ff; margin-bottom: 5px; }
        #dateRangeText { color: #888; font-size: 14px; margin-bottom: 25px; font-style: italic; min-height: 20px; }
        .label { font-size: 13px; color: #aaa; margin-right: -10px; }

        /* --- Bloc sentiment --- */
        #sentimentBlock {
            width: 95%;
            margin: 30px auto 0 auto;
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 28px 32px;
            box-sizing: border-box;
            text-align: left;
        }
        #sentimentBlock h3 {
            color: #00d4ff;
            margin: 0 0 18px 0;
            font-size: 17px;
            text-align: center;
            letter-spacing: 1px;
        }
        .gauge-row {
            display: flex;
            align-items: center;
            gap: 18px;
            margin-bottom: 10px;
        }
        .gauge-bar-wrap {
            flex: 1;
            position: relative;
        }
        .gauge-bar {
            width: 100%;
            height: 22px;
            border-radius: 11px;
            background: linear-gradient(to right, #e74c3c 0%, #95a5a6 50%, #2ecc71 100%);
            position: relative;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.35);
        }
        .gauge-marker {
            position: absolute;
            top: -7px;
            bottom: -7px;
            width: 6px;
            background-color: #ffffff;
            border-radius: 3px;
            box-shadow: 0 0 6px rgba(255,255,255,0.6);
            transition: left 0.5s ease-in-out;
            transform: translateX(-50%);
            left: 50%;
        }
        .gauge-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 7px;
            font-size: 12px;
            color: #777;
        }
        #sentimentScore {
            font-size: 22px;
            font-weight: bold;
            min-width: 70px;
            text-align: center;
        }
        #sentimentBtn {
            background-color: #8e44ad;
            white-space: nowrap;
        }
        #sentimentBtn:hover { background-color: #6c3483; }
        #sentimentStatus {
            font-size: 13px;
            color: #888;
            font-style: italic;
            min-height: 18px;
            margin-bottom: 18px;
            text-align: center;
        }

        /* Liste des articles */
        #newsSection { margin-top: 20px; display: none; }
        #newsSection h4 { color: #aaa; font-size: 14px; margin-bottom: 10px; }
        #newsList { list-style: none; padding: 0; margin: 0; }
        #newsList li {
            background: #111;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 6px;
            border-left: 4px solid #8e44ad;
            font-size: 13px;
            color: #ccc;
            text-align: left;
        }
    </style>
</head>
<body>
    <h2 id="pageTitle">📈 Analyse Graphique & IA</h2>
    <div id="dateRangeText">Initialisation...</div>
    <div class="menu">
        <span class="label">Période:</span>
        <select id="range">
            <option value="1d">1 Jour</option>
            <option value="1mo" selected>1 Mois</option>
            <option value="3mo">3 Mois</option>
            <option value="1y">1 An</option>
        </select>
        <span class="label">Bougies:</span>
        <select id="interval">
            <option value="5m">5 min</option>
            <option value="15m">15 min</option>
            <option value="1h">1 heure</option>
            <option value="1d" selected>1 jour</option>
        </select>
        <button id="refresh">ACTUALISER</button>
        <button id="predictBtn" style="background-color: #ff9800;">PRÉDICTION IA</button>
        <button id ="achat" style="background-color: #2fff006b;">Achat</button>
    </div>
    <div id="chartContainer" style="height: 550px; width: 95%; margin: auto; border-radius: 10px; overflow: hidden;"></div>

    <!-- BLOC SENTIMENT FINBERT -->
    <div id="sentimentBlock">
        <h3>🧠 Analyse de Sentiment FinBERT</h3>
        <div id="sentimentStatus">Appuyez sur le bouton pour analyser le sentiment des actualités.</div>
        <div class="gauge-row">
            <div class="gauge-bar-wrap">
                <div class="gauge-bar">
                    <div class="gauge-marker" id="gaugeMarker"></div>
                </div>
                <div class="gauge-labels">
                    <span>Pessimiste (-1)</span>
                    <span>Neutre (0)</span>
                    <span>Optimiste (+1)</span>
                </div>
            </div>
            <div id="sentimentScore" style="color: #95a5a6;">—</div>
            <button id="sentimentBtn">SENTIMENT</button>
        </div>
        <div id="newsSection">
            <h4>Sources d'actualités analysées :</h4>
            <ul id="newsList"></ul>
        </div>
    </div>

    <script>
    const validIntervals = { "1d": ["5m", "15m", "1h"], "1mo": ["1h", "1d"], "3mo": ["1d"], "1y": ["1d"] };
    const defaultInterval = { "1d": "15m", "1mo": "1d", "3mo": "1d", "1y": "1d" };

    // Lecture du ticker depuis l'URL (?ticker=NVDA), défaut NVDA
    const urlParams = new URLSearchParams(window.location.search);
    const currentSymbol = (urlParams.get('ticker') || 'NVDA').toUpperCase();

    // Titre dynamique
    document.getElementById("pageTitle").innerText = "📈 " + currentSymbol + " — Analyse Graphique & IA";
    document.title = currentSymbol + " - Bourse Expert";

    function updateIntervalOptions() {
        const range = document.getElementById("range").value;
        const intervalSelect = document.getElementById("interval");
        const allowed = validIntervals[range];
        Array.from(intervalSelect.options).forEach(opt => { opt.disabled = !allowed.includes(opt.value); });
        if (!allowed.includes(intervalSelect.value)) { intervalSelect.value = defaultInterval[range]; }
    }

    window.onload = function () {
        var chart = new CanvasJS.Chart("chartContainer", {
            theme: "dark2",
            animationEnabled: true,
            zoomEnabled: true,
            title: { text: "", fontColor: "#00d4ff" },
            axisX: { valueFormatString: "DD MMM HH:mm", crosshair: { enabled: true, snapToDataPoint: true } },
            axisY: { prefix: "$", title: "Prix (USD)", includeZero: false, crosshair: { enabled: true } },
            data: [{ type: "candlestick", yValueFormatString: "$###.00", risingColor: "#26a69a", fallingColor: "#ef5350", dataPoints: [] }]
        });

        async function updateChart() {
            const ran = document.getElementById("range").value;
            const int = document.getElementById("interval").value;
            try {
                const response = await fetch('/api/stock?symbol=' + currentSymbol + '&range=' + ran + '&interval=' + int);
                const result = await response.json();
                if (result.error) throw new Error(result.error);
                chart.options.title.text = "Cours " + currentSymbol;
                chart.options.data[0].dataPoints = result.data.map(p => ({ x: new Date(p.x), y: p.y }));
                chart.render();
                document.getElementById("dateRangeText").innerText = "Graphique mis à jour.";
            } catch (err) {
                document.getElementById("dateRangeText").innerText = "❌ Erreur: " + err.message;
            }
        }

        // Bouton prédiction 2 semaines — INTACT
        document.getElementById("predictBtn").onclick = async function () {
            document.getElementById("dateRangeText").innerText = "Lancement de l'IA pour " + currentSymbol + "...";
            try {
                const response = await fetch('/api/predict?symbol=' + currentSymbol);
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || "Erreur serveur");
                }
                const result = await response.json();
                document.getElementById("dateRangeText").innerText = "🔮 " + result.prediction;
            } catch (err) {
                document.getElementById("dateRangeText").innerText = "❌ Erreur IA : " + err.message;
            }
        };
        document.getElementById("achat").onclick = function() {
            window.location.href = "http://51.38.225.40/trader.php?ticker=" + encodeURIComponent(currentSymbol);
        };

        // Bouton sentiment FinBERT
        document.getElementById("sentimentBtn").onclick = async function () {
            document.getElementById("sentimentStatus").innerText = "⏳ Analyse FinBERT en cours pour " + currentSymbol + "...";
            document.getElementById("sentimentBtn").disabled = true;

            try {
                const response = await fetch('/api/sentiment?symbol=' + currentSymbol);
                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.error || "Erreur serveur Flask");
                }
                const result = await response.json();

                const score = result.score;
                const position = ((score + 1) / 2) * 100;

                document.getElementById("gaugeMarker").style.left = position + "%";

                const scoreEl = document.getElementById("sentimentScore");
                scoreEl.innerText = score.toFixed(2);
                if (score > 0.1) scoreEl.style.color = "#2ecc71";
                else if (score < -0.1) scoreEl.style.color = "#e74c3c";
                else scoreEl.style.color = "#95a5a6";

                document.getElementById("sentimentStatus").innerText = "✅ Analyse terminée pour " + currentSymbol;

                const newsList = document.getElementById("newsList");
                newsList.innerHTML = "";
                result.headlines.forEach(h => {
                    const li = document.createElement("li");
                    li.innerText = h;
                    newsList.appendChild(li);
                });
                document.getElementById("newsSection").style.display = "block";

            } catch (err) {
                document.getElementById("sentimentStatus").innerText = "❌ Erreur : " + err.message;
            } finally {
                document.getElementById("sentimentBtn").disabled = false;
            }
        };

        document.getElementById("range").onchange = () => { updateIntervalOptions(); updateChart(); };
        document.getElementById("refresh").onclick = updateChart;
        document.getElementById("interval").onchange = updateChart;

        updateIntervalOptions();
        updateChart();
    }
    </script>
</body>
</html>
`;

// Route pour les données historiques (Graphique)
app.get('/api/stock', async (req, res) => {
    const { symbol, range, interval } = req.query;
    try {
        let period1 = new Date();
        if (range === '1d') period1.setDate(period1.getDate() - 1);
        else if (range === '1mo') period1.setMonth(period1.getMonth() - 1);
        else if (range === '3mo') period1.setMonth(period1.getMonth() - 3);
        else if (range === '1y') period1.setFullYear(period1.getFullYear() - 1);

        const result = await yahooFinance.chart(symbol, {
            period1: period1,
            period2: new Date(),
            interval: interval
        });

        const dataPoints = result.quotes
            .filter(q => q.open != null && q.close != null)
            .map(q => ({ x: q.date, y: [q.open, q.high, q.low, q.close] }));

        res.json({ data: dataPoints });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Route pour la prédiction IA — INTACT
app.get('/api/predict', (req, res) => {
    const symbol = req.query.symbol;
    const scriptPath = path.join(__dirname, "numeric_prediction.py");

    const env = { ...process.env, PYTHONIOENCODING: "utf-8" };
    const command = `python "${scriptPath}" ${symbol}`;

    console.log(`[DEBUG] Execution: ${command}`);

    exec(command, { cwd: __dirname, env: env }, (error, stdout, stderr) => {
        if (error) {
            console.error("--- ERREUR ---");
            console.error("Msg:", error.message);
            console.error("Stderr:", stderr);
            return res.status(500).json({ error: "Le script Python a crashé. Vérifie ton terminal." });
        }

        let output = stdout.trim();

        if (output.includes("HAUSSIER")) output += " 🚀";
        if (output.includes("BAISSIER")) output += " 📉";

        res.json({ prediction: output });
    });
});

// Route sentiment — proxy vers Flask (app.py sur port 5000)
app.get('/api/sentiment', (req, res) => {
    const symbol = req.query.symbol;
    if (!symbol) return res.status(400).json({ error: "Paramètre symbol manquant" });

    const options = {
        hostname: '127.0.0.1',
        port: FLASK_PORT,
        path: '/api/sentiment?ticker=' + encodeURIComponent(symbol),
        method: 'GET'
    };

    const flaskReq = http.request(options, (flaskRes) => {
        let data = '';
        flaskRes.on('data', chunk => data += chunk);
        flaskRes.on('end', () => {
            try {
                const parsed = JSON.parse(data);
                res.json(parsed);
            } catch (e) {
                res.status(500).json({ error: "Réponse Flask invalide : " + e.message });
            }
        });
    });

    flaskReq.on('error', (e) => {
        console.error("Erreur connexion Flask:", e.message);
        res.status(500).json({ error: "Impossible de joindre Flask (app.py). Est-il démarré sur le port " + FLASK_PORT + " ?" });
    });

    flaskReq.setTimeout(30000, () => {
        flaskReq.abort();
        res.status(504).json({ error: "Timeout : Flask a mis trop longtemps à répondre (FinBERT en cours de chargement ?)" });
    });

    flaskReq.end();
});

// Route principale — accepte ?ticker=XXX
app.get('/', (req, res) => res.send(htmlContent));

app.listen(PORT, '0.0.0.0', () => {
    console.log(`=========================================`);
    console.log(`Serveur actif sur http://0.0.0.0:${PORT}`);
    console.log(`Dossier : ${__dirname}`);
    console.log(`=========================================`);
});