# APK Onboarding & Instruction Flow

This document defines the instructional steps that will be implemented in the Companion APK to guide the user through the setup process.

## Step 1: Environment Setup
**Screen Title**: Termux Installation
**Instructions**:
- "To power the AI, we need a Linux environment on your phone."
- **Action**: Button [Install Termux] $\rightarrow$ Links to F-Droid.
- **Verification**: Checkbox [I have installed Termux].

## Step 2: Hardware Integration
**Screen Title**: Termux:API Setup
**Instructions**:
- "Allow the AI to interact with your system and hardware."
- **Action**: Button [Install Termux:API] $\rightarrow$ Links to F-Droid.
- **Verification**: Checkbox [I have installed Termux:API].

## Step 3: Project Deployment
**Screen Title**: Clone Mobile Companion
**Instructions**:
- "Now, let's pull the core logic into your device."
- **Command to Copy**: 
  ```bash
  git clone https://github.com/agyeiboaduandy-crypto/mobile-companion.git
  cd mobile-companion
  ```
- **Action**: Button [Copy Commands].

## Step 4: System Initialization
**Screen Title**: Run Setup Script
**Instructions**:
- "Initialize the runtimes and install AI tools."
- **Command to Copy**:
  ```bash
  chmod +x scripts/setup_termux.sh
  ./scripts/setup_termux.sh
  ```
- **Action**: Button [Copy Command].

## Step 5: AI Configuration
**Screen Title**: API Key Configuration
**Instructions**:
- "Connect your AI providers to start coding."
- **Action**: Provide a list of keys to set using `ai-keys set KEY_NAME value`.
- **Guide**: Links to `docs/google-ai-studio.md`, etc.

## Step 6: Cloud Persistence
**Screen Title**: GitHub Integration
**Instructions**:
- "Enable the AI to push your code to the cloud."
- **Command to Copy**:
  ```bash
  bash scripts/setup_github.sh
  ```
- **Action**: Button [Copy Command].

## Step 7: Ready to Code
**Screen Title**: Success!
**Instructions**:
- "Your AI coding station is ready."
- **Quick Start**: "Run `ai-open` or `ai-models` in Termux to begin."
