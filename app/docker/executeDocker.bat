cp ..\socket\player_statsV2.py .\player_statsV2.py
docker build -t=socketserver .
docker run -p 50051:50051 socketserver