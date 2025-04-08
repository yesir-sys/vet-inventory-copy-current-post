# Vet Inventory System

## Deployment Instructions

1. Create Heroku account and install Heroku CLI
2. Login to Heroku:
```bash
heroku login
```

3. Create Heroku app:
```bash
heroku create vet-inventory-system
```

4. Push to Heroku:
```bash
git push heroku main
```

5. Set environment variables:
```bash
heroku config:set MONGODB_URI=your_mongodb_uri
```

6. Open the app:
```bash
heroku open
```
