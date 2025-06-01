<h1 align="center"> xAgent </h1>

<div align="center">
 <img alt="anshRS-xAgent-logo" height="200px" src="/assets/logo.png">
</div>

<p align="center">
  Extensible Multitasking Agentic System
</p>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
- [Project Preview](#project-preview)
- [Support](#support)

## Introduction

xAgent is a modular, real-time, intelligent multi-agent mobile application that leverages state-of-the-art language models and clean architecture principles to help users perform tasks across domains like chat, finance, coding, and emailing. The system uses WebSocket communication, LangGraph workflows, and the MCP (Model Context Protocol) design pattern for scalable agent interactions.

## Features

- Secure authentication with JWT
- Profile management with protected routes
- Realtime Chat Agent for general-purpose conversations
- Coding Agent for code generation, debugging, and explanation
- Finance Agent for applying stock strategies and financial analysis
- WebSocket-based real-time communication between agents and backend
- MCP (Model Context Protocol) architecture for modular agent design
- LangGraph based workflow orchestration for stateful task execution
- Clean Architecture and SOLID principles in Flutter frontend
- LLM-powered intelligence using Gemini and LLaMA models

## Tech Stack

| Frontend           | Backend           |  Others           |
| ------------------ | ----------        | ------------------|
| `Dart`             | `Python`          | `Git`             |
| `Flutter`          | `FastAPI`         | `Ollama`          |
| `Bloc`             | `Supabase`        | `Meta Llama`      |
| `GetIt`            | `LangChain`       | `Gemini`          |
| `fpDart`           | `LangGraph`       | `MCP`             |

## Architecture

- The Flutter frontend handles UI interactions and sends/receives data over WebSocket.
- The FastAPI backend acts as the central coordinator, processing real-time messages, managing authentication, and routing requests to agents.
- Agents are modular, LLM-powered components using the Model Context Protocol (MCP) pattern.
- LangGraph is used to orchestrate workflows for certain agents.
- Supabase is used for user authentication and profile data storage via its Python SDK, directly in FastAPI.

<div align="center">
 <img alt="anshRS-xAgent-architecture" src="/assets/architecture.png">
</div>

## Installation

Follow these steps to set up the project locally.

#### Prerequisites

Make sure you have the following installed:

- [Flutter SDK](https://docs.flutter.dev/get-started/install) (v3.x or later)
- [Python](https://www.python.org/downloads/) (v3.10+)
- [Supabase account](https://supabase.com/)
- Git & a code editor

Clone the repository:

```bash
git clone https://github.com/anshRS/xautoflow.git
cd xautoflow
```

#### Backend Setup

Create the virtual environment:

```bash
cd server
python -m venv venv
```

Once created a virtual environment, activate it:

On Windows run:

```bash
venv\Scripts\activate
```

On Unix or MacOS, run:

```bash
source venv/bin/activate
```

Add the dependencies as:

```bash
pip install -r requirements.txt
```

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

Then start the backend server:

```bash
fastapi dev main.py
```

#### Frontend Setup

Ensure your mobile device or emulator is connected properly.

```bash
cd client
flutter pub get
flutter run
```

## Project Preview

Demo video showing the working of the application is provided under `assets/demo.mp4`.

<div align="center">
 <img alt="anshRS-xAgent-preview" src="/assets/preview.png">
</div>

## Support

If you find the project useful or interesting, please consider giving it a ⭐️! Your support is greatly appreciated and helps others discover this project.
