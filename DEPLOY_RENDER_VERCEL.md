# 🚀 Deploy su Render + Vercel - Guida Completa

## 📋 Panoramica

Questa guida ti porterà da zero a un'applicazione online funzionante in 15 minuti usando:
- **Backend**: Render (gratuito)
- **Frontend**: Vercel (gratuito)
- **Dominio**: Il tuo dominio Aruba

## 🎯 STEP 1: Preparazione GitHub

### 1.1 Crea un repository GitHub
```bash
# Nel terminale, nella cartella del progetto
cd /home/nico/Scrivania/finge

# Inizializza git se non esiste
git init

# Aggiungi tutti i file
git add .

# Commit iniziale
git commit -m "Initial commit - Finge app ready for deploy"

# Crea repository su GitHub e collega
git remote add origin https://github.com/TUO_USERNAME/finge.git
git branch -M main
git push -u origin main
```

### 1.2 Verifica che questi file siano presenti:
- ✅ `backend/render.yaml`
- ✅ `frontend/vercel.json`
- ✅ `backend/env.example`
- ✅ `frontend/env.example`

## 🎯 STEP 2: Deploy Backend su Render

### 2.1 Crea account Render
1. Vai su [render.com](https://render.com)
2. Clicca "Get Started for Free"
3. Registrati con GitHub

### 2.2 Deploy del Backend
1. **Dashboard Render** → "New" → "Web Service"
2. **Connect Repository**: Seleziona il tuo repo `finge`
3. **Configurazione**:
   - **Name**: `finge-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

4. **Environment Variables**:
   ```
   FMP_API_KEY = PTFU50sPSAUQugvL9GcAmPAE787UfNBI
   DEBUG = false
   RELOAD = false
   CORS_ORIGINS = https://finge.vercel.app
   ```

5. **Deploy**: Clicca "Create Web Service"

### 2.3 Ottieni URL Backend
- Render ti darà un URL tipo: `https://finge-backend-xxxx.onrender.com`
- **SALVA QUESTO URL** - ti servirà per il frontend

## 🎯 STEP 3: Deploy Frontend su Vercel

### 3.1 Crea account Vercel
1. Vai su [vercel.com](https://vercel.com)
2. Clicca "Sign Up"
3. Registrati con GitHub

### 3.2 Deploy del Frontend
1. **Dashboard Vercel** → "New Project"
2. **Import Git Repository**: Seleziona `finge`
3. **Configure Project**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Environment Variables**:
   ```
   VITE_API_BASE_URL = https://finge-backend-xxxx.onrender.com/api
   ```
   (Sostituisci con il tuo URL Render)

5. **Deploy**: Clicca "Deploy"

### 3.3 Ottieni URL Frontend
- Vercel ti darà un URL tipo: `https://finge-xxxx.vercel.app`
- **SALVA QUESTO URL**

## 🎯 STEP 4: Configurazione Dominio Aruba

### 4.1 Aggiorna CORS su Render
1. Vai su Render Dashboard
2. **finge-backend** → "Environment"
3. Aggiorna `CORS_ORIGINS`:
   ```
   CORS_ORIGINS = https://finge-xxxx.vercel.app,https://app.tuodominio.it
   ```
4. **Redeploy** il servizio

### 4.2 Configura DNS su Aruba
Nel pannello di controllo Aruba:

1. **Aggiungi Record DNS**:
   ```
   Tipo: CNAME
   Nome: app
   Valore: cname.vercel-dns.com
   ```

2. **Aggiungi Record DNS**:
   ```
   Tipo: CNAME  
   Nome: api
   Valore: finge-backend-xxxx.onrender.com
   ```

### 4.3 Configura Dominio su Vercel
1. **Vercel Dashboard** → Il tuo progetto
2. **Settings** → **Domains**
3. **Add Domain**: `app.tuodominio.it`
4. Segui le istruzioni per verificare il dominio

## 🎯 STEP 5: Test Finale

### 5.1 Test Backend
```bash
curl https://api.tuodominio.it/health
# Dovrebbe restituire: {"status": "healthy", "api_key_valid": true}
```

### 5.2 Test Frontend
- Vai su `https://app.tuodominio.it`
- Prova a cercare "AAPL" o "MSFT"
- Verifica che i dati degli analisti appaiano

## 🔧 Troubleshooting

### Problema: CORS Error
**Soluzione**: Aggiorna `CORS_ORIGINS` su Render con il dominio corretto

### Problema: API Key Invalid
**Soluzione**: Verifica che `FMP_API_KEY` sia impostata correttamente su Render

### Problema: Frontend non carica
**Soluzione**: Verifica che `VITE_API_BASE_URL` punti al backend Render

### Problema: Dominio non funziona
**Soluzione**: 
1. Attendi 24-48h per propagazione DNS
2. Verifica configurazione DNS su Aruba
3. Controlla che il dominio sia verificato su Vercel

## 📊 Monitoraggio

### Health Checks:
- Backend: `https://api.tuodominio.it/health`
- Frontend: Accesso diretto al sito

### Logs:
- **Render**: Dashboard → finge-backend → Logs
- **Vercel**: Dashboard → Il tuo progetto → Functions → Logs

## 💰 Costi

- **Render**: Gratuito (con limiti)
- **Vercel**: Gratuito (con limiti)  
- **Dominio**: €10-15/anno (già acquistato)
- **Totale**: €0/mese + costo dominio

## 🚀 Prossimi Passi

1. **Testa tutto** localmente e online
2. **Monitora** i logs per errori
3. **Ottimizza** le performance se necessario
4. **Considera upgrade** a piani a pagamento se hai molto traffico

## 📞 Supporto

Se hai problemi:
1. Controlla i logs su Render/Vercel
2. Verifica le variabili d'ambiente
3. Testa gli endpoint con curl
4. Controlla la configurazione DNS

---

**🎉 Congratulazioni! La tua app è online!**
