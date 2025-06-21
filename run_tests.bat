@echo off
setlocal

echo  Docker test container baslatiliyor.....

docker-compose run --rm test_runner


echo Random user creation completed. Test logu test_output.txt dosyasindadir.
endlocal