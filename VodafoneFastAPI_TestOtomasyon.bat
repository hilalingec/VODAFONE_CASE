@echo off
setlocal 

echo VODAFONE TEST OTOMASYONU BAŞLADI

echo [1/4] FastAPI servisleri baslatiliyor... 

call run_fastapi_project.bat -d 

echo  Docker random isim uretme test container'ı baslatiliyor.....

call run_tests.bat -d
call run_tests.bat -d
call run_tests.bat -d
call run_tests.bat -d
call run_tests.bat -d


echo Random user creation tamamlanmistir. 

echo [2/4] Mevcut veriler MySQL'den okunuyor... 
echo.
echo --- MySQL 'person' tablosu ---
docker exec mysql_server sh -c "mysql -uroot -proot -e \"USE test_db; SELECT * FROM person;\""


echo.
echo Bu listedeki ID lerden birini secin.
set /p ID= Kontrol edilecek kullanici ID'si: 
echo Secilen ID: %ID% 

echo [3/4] GET /user/!ID! getiriliyor (ilk kez)... 
curl http://localhost:8000/user/%ID% 

echo.
echo 65 saniye bekleniyor... 
timeout /t 65 >nul

echo [4/4] GET /user/!ID! getiriliyor  (ikinci kez - Kesinlikle MySQL'den cekecek)... 
curl http://localhost:8000/user/%ID% 


echo [4/4] GET /user/!ID! getiriliyor  (ucuncu kez - Kesinlikle Redis'ten cekecek)... 
curl http://localhost:8000/user/%ID% 

echo  .
echo  .

echo  Test tamamlanmistir.
pause
endlocal