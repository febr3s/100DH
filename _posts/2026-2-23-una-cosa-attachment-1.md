---
title: setting up SHH for github on ubuntu or WSL
tags: guides, linux, github
ai: https://chat.deepseek.com/share/f7btyg2j6lehl1wrq9
---

# Guide

Here's how to set up ubuntu or WSL to push to GitHub via SSH:

Note:  if SHH is already set up in your current workstation jump to step 6

1. **Check Git identity** (skip if already set):
   ```bash
   git config --global user.name   # shows current name if set
   git config --global user.email  # shows current email if set
   ```
   
   Set them if needed:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your_email@example.com"
   ```

2. **Generate SSH key** (creates public/private key pair for GitHub auth):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept default location, Enter again for no passphrase (optional)
   ```
3. **Copy public key** (this goes on GitHub):
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # Select and copy the entire output
   ```

4. **Add to GitHub** (tell GitHub to trust your computer):
   - Go to [github.com/settings/keys](https://github.com/settings/keys)
   - "New SSH key", paste, save

5. **Test connection** (verify everything works):
   ```bash
   ssh -T git@github.com
   # Should see "febr3s@DESKTOP-12IT2VB:~/wa-gbAPI-gatekeeping$    ssh -T git@github.com 
   The authenticity of host 'github.com (140.82.114.4)' can't be established.
   ED25519 key fingerprint is **********************************
   This key is not known by any other names.
   Are you sure you want to continue connecting (yes/no/[fingerprint])?"
   ```
   Enter  ´yes´

6. **Use SSH URLs** (instead of HTTPS):

    ### Check what you're using now
    ```bash
    git remote -v
    ```
    (Probably shows: https://github.com/eduardofebresm/something.git)

    ### Switch it to SSH
    
    ```bash
    git remote set-url origin git@github.com:eduardofebresm/something.git
    ```

Now you can `git push` without passwords.

## For organization repos

The procedure is **exactly the same** as for your personal repos.  
Since you already set up SSH for your GitHub user, and you own the organization, you already have access.

1. **Get the SSH URL** of the organization repo (not HTTPS).  
   Example: `git@github.com:your-organization/repo-name.git`

2. **Update your local repo’s remote** (if it’s already cloned via HTTPS):  
   ```bash
   git remote set-url origin git@github.com:your-organization/repo-name.git
   ```

3. **Push as usual**:  
   ```bash
   git push
   ```

That’s it. SSH authentication works the same regardless of whether the repo belongs to you or your organization—it’s tied to your GitHub user account, not the repo owner.

# Explanation

## Step 2: `ssh-keygen`
**What**: Creates two files: a **private key** (`id_ed25519`) and a **public key** (`id_ed25519.pub`) in `~/.ssh/`
**Why**: SSH uses cryptographic keys instead of passwords. The public key goes on GitHub, the private key stays on your computer. When you connect, GitHub checks if your private key matches the public key they have.

## Step 3: `cat ~/.ssh/id_ed25519.pub`
**What**: Displays your public key in the terminal so you can copy it.
**Why**: You need to give this key to GitHub. It's safe to share - it's like a lock that only your private key can open.

## Step 4: Add to GitHub
**What**: You paste your public key into GitHub's web interface.
**Why**: This tells GitHub "this public key belongs to me." Later, when you connect with your private key, GitHub recognizes you.

## Step 5: `ssh -T git@github.com`
**What**: Makes a test SSH connection to GitHub.
**Why**: Confirms everything is working. GitHub sends back a message saying "I recognize you, here's your username."

## Step 6: Use SSH URLs
**What**: Instead of `https://github.com/...`, you use `git@github.com:...` for your repos.
**Why**: HTTPS URLs would ask for username/password (or personal access token). SSH URLs automatically use your SSH key for authentication.

The magic: When you `git push`, Git uses SSH to connect to GitHub. SSH sees you have the private key, GitHub checks it matches your public key, and access is granted automatically.