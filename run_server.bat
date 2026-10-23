@echo off
title Restaurant Food Ordering System - DBMS Course Project
echo ===============================================================
echo   Restaurant Food Ordering System (DBMS Project)
echo   Connected to MySQL Database: restaurant_food_ordering
echo ===============================================================
echo.
echo Starting Django Development Server on all interfaces (0.0.0.0:8000)...
echo.
echo Access on this computer:
echo   --^> http://127.0.0.1:8000/
echo.
echo Access from other devices / phones on the same Wi-Fi:
echo   --^> http://172.16.33.207:8000/
echo.
echo Press Ctrl+C in this window to stop the server.
echo.
python manage.py runserver 0.0.0.0:8000
pause
