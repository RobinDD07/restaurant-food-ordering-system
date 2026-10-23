@echo off
title Restaurant Food Ordering System - DBMS Course Project
echo ===============================================================
echo   Restaurant Food Ordering System (DBMS Project)
echo   Connected to MySQL Database: restaurant_food_ordering
echo ===============================================================
echo.
echo Starting Django Development Server...
echo Open your web browser and navigate to:
echo   --^> http://127.0.0.1:8000/
echo.
echo Press Ctrl+C in this terminal window to stop the server.
echo.
python manage.py runserver 127.0.0.1:8000
pause
