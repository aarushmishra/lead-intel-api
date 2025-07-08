# 🔌 Postman cURL Commands (Cloud Deployment)

## 🌐 **Replace `YOUR_APP_URL` with your actual deployed URL**

Examples:
- Railway: `https://lead-intel-api-production.up.railway.app`
- Render: `https://lead-intel-api.onrender.com`
- Heroku: `https://lead-intel-api.herokuapp.com`

---

## **1. Health Check**
```bash
curl --location 'https://YOUR_APP_URL/health' \
--header 'Content-Type: application/json'
```

## **2. Enrich Lead - High Value College (ADYPU)**
```bash
curl --location 'https://YOUR_APP_URL/enrich_lead' \
--header 'Content-Type: application/json' \
--data '{
    "college": "ADYPU",
    "city": "Pune",
    "state": "Maharashtra",
    "course": "BBA",
    "language": "Hindi"
}'
```

## **3. Enrich Lead - Medium Value College (MIT)**
```bash
curl --location 'https://YOUR_APP_URL/enrich_lead' \
--header 'Content-Type: application/json' \
--data '{
    "college": "MIT",
    "city": "Pune",
    "state": "Maharashtra",
    "course": "B.Tech",
    "language": "English"
}'
```

## **4. Enrich Lead - Low Value College (RBU)**
```bash
curl --location 'https://YOUR_APP_URL/enrich_lead' \
--header 'Content-Type: application/json' \
--data '{
    "college": "RBU",
    "city": "Greater Noida",
    "state": "Uttar Pradesh",
    "course": "MBA",
    "language": "Hinglish"
}'
```

## **5. Enrich Lead - City Only (Ghaziabad)**
```bash
curl --location 'https://YOUR_APP_URL/enrich_lead' \
--header 'Content-Type: application/json' \
--data '{
    "college": "",
    "city": "Ghaziabad",
    "state": "Uttar Pradesh",
    "course": "BBA",
    "language": "Hindi"
}'
```

## **6. Enrich Lead - Nurture Fallback**
```bash
curl --location 'https://YOUR_APP_URL/enrich_lead' \
--header 'Content-Type: application/json' \
--data '{
    "college": "",
    "city": "",
    "state": "Tamil Nadu",
    "course": "B.Tech",
    "language": ""
}'
```

## **7. Enrich Lead - Different Language (Marathi)**
```bash
curl --location 'https://YOUR_APP_URL/enrich_lead' \
--header 'Content-Type: application/json' \
--data '{
    "college": "SAGE",
    "city": "Mumbai",
    "state": "Maharashtra",
    "course": "MBA",
    "language": "Marathi"
}'
```

## **8. API Documentation**
```bash
curl --location 'https://YOUR_APP_URL/docs' \
--header 'Content-Type: application/json'
```

---

## 📋 **Postman Environment Setup**

### **Environment Variables**
Create a Postman environment with:
- `base_url`: `https://YOUR_APP_URL`
- `api_key`: (if needed in future)

### **Collection Structure**
```
Lead Intel API (Cloud)
├── Health Check
│   └── GET {{base_url}}/health
├── Enrich Lead
│   ├── High Value College
│   ├── Medium Value College
│   ├── Low Value College
│   ├── City Only
│   ├── Nurture Fallback
│   └── Different Languages
└── API Documentation
    └── GET {{base_url}}/docs
```

---

## 🎯 **Expected Responses**

### **High Value College Response:**
```json
{
  "college": "ADYPU",
  "city": "Pune",
  "state": "Maharashtra",
  "course": "BBA",
  "language": "Hindi",
  "caller_name": "Priya Sharma",
  "pitch_text": "Hi, I'm calling from Ajeenkya DY Patil University. I noticed you're interested in BBA. Would you like to know more about our programs?",
  "tts_languages": ["Hindi", "English"]
}
```

### **Medium Value College Response:**
```json
{
  "college": "MIT",
  "city": "Pune",
  "state": "Maharashtra",
  "course": "B.Tech",
  "language": "English",
  "caller_name": "Sunstone Advisor",
  "pitch_text": "Hi, I'm calling from Pune MIT College. I noticed you're interested in B.Tech. Would you like to explore our programs?",
  "tts_languages": ["English"]
}
```

### **Low Value College Response:**
```json
{
  "college": "RBU",
  "city": "Greater Noida",
  "state": "Uttar Pradesh",
  "course": "MBA",
  "language": "Hinglish",
  "caller_name": "Sunstone Advisor",
  "pitch_text": "Hi, I'm calling from Sunstone in Greater Noida. I noticed you're interested in MBA. Would you like to know more about our programs?",
  "tts_languages": ["Hinglish", "English"]
}
```

---

## 🚀 **Quick Test Steps**

1. **Deploy to cloud** (Railway/Render/Heroku)
2. **Get your app URL**
3. **Replace `YOUR_APP_URL`** in all cURL commands
4. **Test health check first**
5. **Test lead enrichment**
6. **Verify responses match expected format**

---

## 🔧 **Troubleshooting**

### **If Health Check Fails:**
```bash
# Check if app is deployed
curl -I https://YOUR_APP_URL/health

# Check logs in your cloud platform dashboard
# Common issues: port configuration, dependencies, environment variables
```

### **If API Returns Errors:**
```bash
# Check the response for error details
curl -v https://YOUR_APP_URL/enrich_lead \
  -H "Content-Type: application/json" \
  -d '{"state": "Maharashtra", "course": "BBA"}'
```

---

**🎯 Your Lead Intel API is now accessible from anywhere in the world!** 