# ✅ Checklist Deploy Render + Vercel

## 📋 Pre-Deploy (Completato ✅)

- [x] Codice preparato e committato
- [x] File di configurazione creati
- [x] Script di preparazione eseguito
- [x] Repository GitHub configurato

## 🎯 STEP 1: GitHub Repository

### 1.1 Crea Repository GitHub
- [ ] Vai su [github.com](https://github.com)
- [ ] Clicca "New repository"
- [ ] Nome: `finge`
- [ ] Pubblica il repository
- [ ] Collega il repository locale:
  ```bash
  git remote add origin https://github.com/TUO_USERNAME/finge.git
  git branch -M main
  git push -u origin main
  ```

## 🎯 STEP 2: Backend su Render

### 2.1 Account Render
- [ ] Vai su [render.com](https://render.com)
- [ ] Registrati con GitHub
- [ ] Verifica email

### 2.2 Deploy Backend
- [ ] Dashboard → "New" → "Web Service"
- [ ] "Connect Repository" → Seleziona `finge`
- [ ] **Configurazione**:
  - [ ] Name: `finge-backend`
  - [ ] Environment: `Python 3`
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
  - [ ] Plan: `Free`

### 2.3 Environment Variables
- [ ] `FMP_API_KEY` = `PTFU50sPSAUQugvL9GcAmPAE787UfNBI`
- [ ] `DEBUG` = `false`
- [ ] `RELOAD` = `false`
- [ ] `CORS_ORIGINS` = `https://finge.vercel.app`

### 2.4 Deploy
- [ ] Clicca "Create Web Service"
- [ ] Attendi il deploy (5-10 minuti)
- [ ] **SALVA L'URL**: `https://finge-backend-xxxx.onrender.com`

## 🎯 STEP 3: Frontend su Vercel

### 3.1 Account Vercel
- [ ] Vai su [vercel.com](https://vercel.com)
- [ ] Registrati con GitHub
- [ ] Verifica email

### 3.2 Deploy Frontend
- [ ] Dashboard → "New Project"
- [ ] "Import Git Repository" → Seleziona `finge`
- [ ] **Configurazione**:
  - [ ] Framework Preset: `Vite`
  - [ ] Root Directory: `frontend`
  - [ ] Build Command: `npm run build`
  - [ ] Output Directory: `dist`

### 3.3 Environment Variables
- [ ] `VITE_API_BASE_URL` = `https://finge-backend-xxxx.onrender.com/api`
  (Sostituisci con il tuo URL Render)

### 3.4 Deploy
- [ ] Clicca "Deploy"
- [ ] Attendi il deploy (2-3 minuti)
- [ ] **SALVA L'URL**: `https://finge-xxxx.vercel.app`

## 🎯 STEP 4: Aggiorna CORS

### 4.1 Aggiorna Render
- [ ] Vai su Render Dashboard
- [ ] `finge-backend` → "Environment"
- [ ] Aggiorna `CORS_ORIGINS`:
  ```
  https://finge-xxxx.vercel.app,https://app.tuodominio.it
  ```
- [ ] Clicca "Save Changes"
- [ ] Attendi il redeploy

## 🎯 STEP 5: Dominio Aruba

### 5.1 DNS Records
Nel pannello Aruba, aggiungi:

- [ ] **CNAME Record**:
  - Nome: `app`
  - Valore: `cname.vercel-dns.com`

- [ ] **CNAME Record**:
  - Nome: `api`
  - Valore: `finge-backend-xxxx.onrender.com`

### 5.2 Configura Vercel
- [ ] Vercel Dashboard → Il tuo progetto
- [ ] Settings → Domains
- [ ] Add Domain: `app.tuodominio.it`
- [ ] Segui le istruzioni per verificare

## 🎯 STEP 6: Test Finale

### 6.1 Test Backend
- [ ] `curl https://api.tuodominio.it/health`
- [ ] Dovrebbe restituire: `{"status": "healthy", "api_key_valid": true}`

### 6.2 Test Frontend
- [ ] Vai su `https://app.tuodominio.it`
- [ ] Prova a cercare "AAPL"
- [ ] Verifica che appaiano i dati degli analisti
- [ ] Controlla che il sistema di scoring funzioni

### 6.3 Test Completo
- [ ] Cerca diverse aziende (MSFT, GOOGL, etc.)
- [ ] Verifica che i suggerimenti degli analisti appaiano
- [ ] Controlla che tutto sia responsive

## 🎯 STEP 7: Monitoraggio

### 7.1 Health Checks
- [ ] Backend: `https://api.tuodominio.it/health`
- [ ] Frontend: Accesso diretto al sito

### 7.2 Logs
- [ ] Render: Dashboard → finge-backend → Logs
- [ ] Vercel: Dashboard → Il tuo progetto → Functions → Logs

## 🚨 Troubleshooting

### CORS Error
- [ ] Verifica `CORS_ORIGINS` su Render
- [ ] Assicurati che includa il dominio Vercel

### API Key Invalid
- [ ] Controlla `FMP_API_KEY` su Render
- [ ] Verifica che sia impostata correttamente

### Frontend non carica
- [ ] Verifica `VITE_API_BASE_URL` su Vercel
- [ ] Controlla che punti al backend Render

### Dominio non funziona
- [ ] Attendi 24-48h per propagazione DNS
- [ ] Verifica configurazione DNS su Aruba
- [ ] Controlla che il dominio sia verificato su Vercel

## 🎉 Completato!

- [ ] App online e funzionante
- [ ] Dominio configurato
- [ ] SSL attivo
- [ ] Monitoraggio configurato

---

**🎊 Congratulazioni! La tua app Finge è online!**

**URL Finali:**
- Frontend: `https://app.tuodominio.it`
- Backend: `https://api.tuodominio.it`
- Health Check: `https://api.tuodominio.it/health`

