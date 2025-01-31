#!/bin/bash
brew services start redis
celery -A tasks worker --loglevel=info