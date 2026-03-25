---
title: creating hidden keys for applications
---

Today I was coding the Telegram script to push posts. I neededed to use a key while having a public repo. I co-created this guide with DeepSeek.

## The Environment Variable Method (Simplified)

This method keeps your secret keys out of your public repository by storing them in environment variables. You'll use a local `.env` file for development and set real environment variables on your deployment platform.

---

### Step 1: Create a local `.env` file
In your project folder, create a file named `.env`. Put your secret key inside, like this:
```
API_KEY=your-super-secret-key-here
```
This file will **never** be uploaded to GitHub.

---

### Step 2: Tell Git to ignore `.env`
Create a file named `.gitignore` (if you don't have one) and add this line:
```
.env
```
Now Git will ignore your `.env` file. You can check with `git status` – it shouldn’t appear.

---

### Step 3: Create a template file for others
Create a file named `.env.example` with the same variable names but placeholder values:
```
API_KEY=your-api-key-here
```
Commit this file to your repository. Anyone who clones your project can copy `.env.example` to `.env` and fill in their own real key.

---

### Step 4: Read the environment variable in your code
Your application should read the key from the environment. How you do this depends on your language, but the idea is the same:

- **Python:** `os.getenv('API_KEY')`
- **Ruby:** `ENV['API_KEY']`
- **Go:** `os.Getenv("API_KEY")`
- **Java:** `System.getenv("API_KEY")`
- **Bash:** `$API_KEY`

During development, you can load the `.env` file using a simple library (like `python-dotenv` for Python, `dotenv` for Ruby, etc.) so that the variables are automatically available in your code.

---

### Step 5: Set environment variables on your deployment platform
When you deploy your app (to Heroku, AWS, DigitalOcean, etc.), you **do not** upload the `.env` file. Instead, you set the same variables through the platform’s interface. Examples:

- **Heroku:** `heroku config:set API_KEY=your-super-secret-key-here`
- **GitHub Actions:** Add a secret named `API_KEY` in your repo settings
- **Vercel / Netlify:** Use their dashboard to add environment variables
- **Docker:** Pass with `-e API_KEY=...` or use an orchestration tool

Your code reads the variable the same way – from the environment – so it works identically in development and production.

---

### Why this works
- The real key never appears in your repository.
- Other developers know which variables are needed from the `.env.example` file.
- Deployment platforms keep your keys secure and inject them at runtime.