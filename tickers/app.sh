#!/bin/bash
(trap 'kill 0' SIGINT EXIT; ./app.py & ./spawn.py)
