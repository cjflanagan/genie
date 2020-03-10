source .env
psql postgresql://postgres:genie1234@localhost:5432/genie
nohup flask run --host 0.0.0.0 > server.out &
