#!/bin/bash
echo "Stopping StratIQ..."
docker stop stratiq && docker rm stratiq
echo "Done. Your data is preserved in the stratiq_data volume."
